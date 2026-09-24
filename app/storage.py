from __future__ import annotations
from pathlib import Path
from uuid import uuid4
import boto3
from botocore.config import Config as BotoConfig
from flask import current_app

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.mp4', '.webm', '.mov'}
VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov'}

def _b2_enabled() -> bool:
    cfg = current_app.config
    return bool(cfg.get('B2_KEY_ID') and cfg.get('B2_APPLICATION_KEY') and cfg.get('B2_BUCKET_NAME'))

def _client():
    cfg = current_app.config
    return boto3.client('s3', endpoint_url=cfg['B2_ENDPOINT_URL'], aws_access_key_id=cfg['B2_KEY_ID'], aws_secret_access_key=cfg['B2_APPLICATION_KEY'], region_name=cfg['B2_REGION'], config=BotoConfig(signature_version='s3v4'))

def _safe_extension(filename: str) -> str | None:
    ext = Path(filename).suffix.lower()
    return ext if ext in ALLOWED_EXTENSIONS else None

def save_image(file_storage, prefix: str) -> str | None:
    if not file_storage or not file_storage.filename:
        return None
    ext = _safe_extension(file_storage.filename)
    if not ext:
        return None
    if prefix.startswith('user_'):
        key = f"profile/{prefix}/{uuid4().hex}{ext}"
    elif prefix.startswith('pastor'):
        key = f"profile/pastors/{uuid4().hex}{ext}"
    elif prefix.startswith('announcement'):
        key = f"announcements/{uuid4().hex}{ext}"
    else:
        key = f"images/{prefix}_{uuid4().hex}{ext}"
    if _b2_enabled():
        content_type = file_storage.mimetype or ('video/mp4' if ext == '.mp4' else 'application/octet-stream')
        _client().upload_fileobj(file_storage, current_app.config['B2_BUCKET_NAME'], key, ExtraArgs={'ContentType': content_type})
        return key
    destination = Path(current_app.config['UPLOAD_FOLDER']) / key
    destination.parent.mkdir(parents=True, exist_ok=True)
    file_storage.save(destination)
    return key

def delete_image(key: str | None) -> None:
    if not key:
        return
    if _b2_enabled():
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
    if _b2_enabled():
        return _client().generate_presigned_url('get_object', Params={'Bucket': current_app.config['B2_BUCKET_NAME'], 'Key': key}, ExpiresIn=current_app.config['B2_PRESIGNED_URL_SECONDS'])
    return f"/static/uploads/{key}"
