# Perfis e Contas

## Tipos
O projeto possui dois níveis principais:
- Usuário/membro.
- Administrador.

## Perfil do usuário
O usuário poderá ter:
- nome;
- e-mail;
- foto;
- dados de perfil permitidos pelo sistema.

## Foto
A foto deve ser enviada para o serviço de armazenamento configurado, e o banco deve guardar a referência necessária.

## Sair x excluir
**Sair:** encerra a sessão.

**Excluir conta:** remove a conta de acordo com as regras de exclusão do sistema e deve exigir confirmação.

## Segurança
Permissões são verificadas no servidor. Esconder um botão no frontend não é suficiente para proteger uma função.
