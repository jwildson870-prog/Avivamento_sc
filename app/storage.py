from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import boto3
from botocore.config import Config as BotoConfig
from flask import current_app

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_MEDIA_EXTENSIONS = ALLOWED_EXTENSIONS | {'.mp4', '.webm', '.ogg'}

def _b2_enabled() -> bool:
    cfg = current_app.config
    return bool(cfg.get('B2_KEY_ID') and cfg.get('B2_APPLICATION_KEY') and cfg.get('B2_BUCKET_NAME'))

def _client():
    cfg = current_app.config
    return boto3.client(
        's3',
        endpoint_url=cfg['B2_ENDPOINT_URL'],
        aws_access_key_id=cfg['B2_KEY_ID'],
        aws_secret_access_key=cfg['B2_APPLICATION_KEY'],
        region_name=cfg['B2_REGION'],
        config=BotoConfig(signature_version='s3v4'),
    )

def _safe_extension(filename: str) -> str | None:
    ext = Path(filename).suffix.lower()
    return ext if ext in ALLOWED_EXTENSIONS else None

def save_media(file_storage, prefix: str, allow_video: bool = False) -> str | None:
    if not file_storage or not file_storage.filename:
        return None
    ext = Path(file_storage.filename).suffix.lower()
    allowed = ALLOWED_MEDIA_EXTENSIONS if allow_video else ALLOWED_EXTENSIONS
    if ext not in allowed:
        return None
    key = f"media/{prefix}/{uuid4().hex}{ext}"
    if _b2_enabled():
        content_type = file_storage.mimetype or 'application/octet-stream'
        try:
            _client().upload_fileobj(
                file_storage,
                current_app.config['B2_BUCKET_NAME'],
                key,
                ExtraArgs={'ContentType': content_type},
            )
        except Exception:
            current_app.logger.exception('Falha ao enviar arquivo para o Backblaze B2: %s', key)
            return None
        return key
    destination = Path(current_app.config['UPLOAD_FOLDER']) / key
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_storage.save(destination)
    return key

def save_image(file_storage, prefix: str) -> str | None:
    if not file_storage or not file_storage.filename:
        return None
    ext = _safe_extension(file_storage.filename)
    if not ext:
        return None
    key = f"profile/{prefix}/{uuid4().hex}{ext}" if prefix.startswith('user_') else f"images/{prefix}_{uuid4().hex}{ext}"
    if _b2_enabled():
        content_type = file_storage.mimetype or 'application/octet-stream'
        try:
            _client().upload_fileobj(
                file_storage,
                current_app.config['B2_BUCKET_NAME'],
                key,
                ExtraArgs={'ContentType': content_type},
            )
        except Exception:
            current_app.logger.exception('Falha ao enviar imagem para o Backblaze B2: %s', key)
            return None
        return key
    destination = Path(current_app.config['UPLOAD_FOLDER']) / key
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_storage.save(destination)
    return key

def delete_image(key: str | None) -> None:
    if not key:
        return
    if _b2_enabled() and (key.startswith('images/') or key.startswith('media/') or key.startswith('profile/')):
        try:
            _client().delete_object(Bucket=current_app.config['B2_BUCKET_NAME'], Key=key)
        except Exception:
            current_app.logger.exception('Falha ao apagar imagem do Backblaze B2: %s', key)
        return
    path = Path(current_app.config['UPLOAD_FOLDER']) / key
    if path.exists():
        path.unlink()

def image_url(key: str | None) -> str | None:
    if not key:
        return None
    if _b2_enabled() and (key.startswith('images/') or key.startswith('media/') or key.startswith('profile/')):
        try:
            return _client().generate_presigned_url(
                'get_object',
                Params={'Bucket': current_app.config['B2_BUCKET_NAME'], 'Key': key},
                ExpiresIn=current_app.config['B2_PRESIGNED_URL_SECONDS'],
            )
        except Exception:
            current_app.logger.exception('Falha ao gerar URL do Backblaze B2: %s', key)
            return None
    return f"/static/uploads/{key}"
