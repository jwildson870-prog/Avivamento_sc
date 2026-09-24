# Igreja Avivamento — PWA

Projeto inicial em Flask para o site da Igreja Avivamento.

## Incluído
- PWA instalável com ícone baseado na imagem fornecida.
- Visual preto, branco e cinza, com azul claro para ações de entrada e vermelho para ações destrutivas.
- Login, cadastro e perfis.
- Upload de foto de perfil.
- Área pública com biografia da igreja e pastores.
- Área administrativa protegida por papel (`admin`).
- CRUD de pastores: adicionar, editar e excluir.
- Edição da biografia da igreja pelo admin.
- Listagem de usuários para admin.
- Exclusão de conta do membro por botão explícito.
- `Sair` encerra a sessão sem apagar a conta, evitando exclusão acidental.

## Executar
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Abra `http://localhost:5000`.

## Admin inicial de desenvolvimento
- usuário: `admin`
- e-mail: `admin@avivamento.local`
- senha: `admin123`

Troque a senha/chave antes de colocar em produção.


## Integrações de produção

- PostgreSQL: Neon, via `DATABASE_URL`.
- Arquivos e imagens: Backblaze B2, via API S3-compatible.
- Servidor: Render, com `gunicorn run:app`.

Nunca commite credenciais do Neon, Backblaze ou `SECRET_KEY`.
