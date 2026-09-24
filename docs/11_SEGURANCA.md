# Segurança

## Regras básicas
- HTTPS em produção.
- Senhas com hash seguro.
- Segredos em variáveis de ambiente.
- Proteção de sessões.
- Autorização no backend.
- Validação de entradas.
- Limites para uploads.
- Proteção contra acesso indevido ao painel administrativo.

## Conta
`Sair` não exclui conta.

`Excluir conta` é uma ação destrutiva e deve exigir confirmação.

## Produção
Antes do lançamento, revisar:
- SECRET_KEY;
- credenciais do PostgreSQL;
- credenciais do armazenamento;
- cookies e sessão;
- CORS, se utilizado;
- logs e mensagens de erro.

## Atualização
Toda nova funcionalidade que manipule dados ou permissões deve receber uma seção de segurança aqui.

## Proteção CSRF

A aplicação utiliza `Flask-WTF` com `CSRFProtect` para proteger requisições `POST`. Todos os formulários POST do sistema enviam um token CSRF e requisições com token ausente, inválido ou expirado são bloqueadas com HTTP 400.

A proteção cobre autenticação, cadastro, perfil, uploads e ações administrativas, incluindo alterações e exclusões.
