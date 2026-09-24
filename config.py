import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'troque-esta-chave-em-producao')

    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = 'postgresql+psycopg://' + database_url[len('postgres://'):]
        elif database_url.startswith('postgresql://'):
            database_url = 'postgresql+psycopg://' + database_url[len('postgresql://'):]
    SQLALCHEMY_DATABASE_URI = database_url or f"sqlite:///{BASE_DIR / 'instance' / 'avivamento.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    UPLOAD_FOLDER = BASE_DIR / 'app' / 'static' / 'uploads'

    B2_KEY_ID = os.environ.get('B2_KEY_ID')
    B2_APPLICATION_KEY = os.environ.get('B2_APPLICATION_KEY')
    B2_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME', 'Avivamento')
    B2_ENDPOINT_URL = os.environ.get('B2_ENDPOINT_URL', 'https://s3.us-east-005.backblazeb2.com')
    B2_REGION = os.environ.get('B2_REGION', 'us-east-005')
    B2_PRESIGNED_URL_SECONDS = int(os.environ.get('B2_PRESIGNED_URL_SECONDS', '3600'))

    INITIAL_ADMIN_USERNAME = os.environ.get('INITIAL_ADMIN_USERNAME', 'admin')
    INITIAL_ADMIN_EMAIL = os.environ.get('INITIAL_ADMIN_EMAIL', 'admin@avivamento.local')
    INITIAL_ADMIN_PASSWORD = os.environ.get('INITIAL_ADMIN_PASSWORD')
