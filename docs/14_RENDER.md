# Render

- Tipo: Web Service
- Branch: `main`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn run:app`
- Auto-Deploy: habilitado

## Variáveis

- `SECRET_KEY`
- `DATABASE_URL` — conexão do Neon
- `B2_KEY_ID`
- `B2_APPLICATION_KEY`
- `B2_BUCKET_NAME=Avivamento`
- `B2_ENDPOINT_URL=https://s3.us-east-005.backblazeb2.com`
- `B2_REGION=us-east-005`
- `INITIAL_ADMIN_USERNAME`
- `INITIAL_ADMIN_EMAIL`
- `INITIAL_ADMIN_PASSWORD`

`INITIAL_ADMIN_PASSWORD` nunca deve ser commitada.
