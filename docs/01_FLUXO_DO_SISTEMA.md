# Fluxo do Sistema — Igreja Avivamento

## Objetivo
Este documento explica o fluxo geral do site, desde a entrada do visitante até as áreas autenticadas.

## Fluxo público
1. Visitante acessa o site.
2. O Flask entrega a página inicial.
3. O visitante pode consultar a apresentação, biografia da igreja e pastores.
4. O visitante pode entrar ou criar uma conta.

## Fluxo de autenticação
1. Usuário abre Login/Cadastro.
2. O Flask valida os dados.
3. A senha é armazenada somente em formato de hash.
4. Após o login, a sessão identifica o usuário.
5. O sistema verifica o papel da conta: usuário ou administrador.
6. Cada papel recebe somente as áreas permitidas.

## Fluxo do administrador
1. Administrador entra.
2. O sistema verifica a permissão de administrador no servidor.
3. O painel administrativo é liberado.
4. O administrador pode gerenciar conteúdos e usuários conforme as regras do sistema.

## Fluxo do perfil
1. Usuário abre Perfil.
2. Pode alterar dados permitidos e foto.
3. `Sair` encerra a sessão.
4. `Excluir minha conta` é uma ação separada e destrutiva.

> Regra importante: sair nunca deve excluir a conta automaticamente.

## Regra de atualização
Quando o fluxo mudar, este README deve ser atualizado junto com o código.
