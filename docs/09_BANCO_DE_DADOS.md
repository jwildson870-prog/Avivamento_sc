# Banco de Dados

## Banco definido
O projeto não usa Supabase.

A arquitetura planejada utiliza **PostgreSQL** como banco de dados.

## Responsabilidades
O banco guarda dados estruturados, como:
- usuários;
- perfis;
- pastores;
- conteúdo institucional;
- configurações necessárias.

## Princípios
- Senhas nunca são armazenadas em texto puro.
- Segredos e credenciais ficam em variáveis de ambiente.
- Alterações de esquema devem ser documentadas.
- Migrações devem ser reproduzíveis.

## Produção
A instância PostgreSQL usada em produção deve ser gerenciada separadamente do código da aplicação.

## Atualização
Cada mudança de tabela, coluna, índice ou relacionamento deve ser registrada aqui.
