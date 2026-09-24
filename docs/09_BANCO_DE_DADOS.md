# Banco de dados

## Produção

O projeto usa **PostgreSQL externo no Neon**. A conexão é fornecida pela variável `DATABASE_URL`.

O código converte URLs `postgres://`/`postgresql://` para o driver `psycopg` usado pelo SQLAlchemy.

## Desenvolvimento local

Sem `DATABASE_URL`, o projeto usa SQLite local em `instance/avivamento.db`.

Nunca coloque `DATABASE_URL` ou senhas do Neon no GitHub.
