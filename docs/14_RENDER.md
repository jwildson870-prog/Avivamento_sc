# Deploy no Render

## Aplicação
O Render será o servidor de execução da aplicação Flask/Python.

## Configuração
O serviço deve obter:
- código pelo GitHub;
- dependências pelo `requirements.txt`;
- configurações sensíveis por variáveis de ambiente;
- conexão com PostgreSQL por variável de conexão segura.

## Banco
O PostgreSQL deve ser externo ao processo da aplicação e persistente.

## Produção
Antes do primeiro lançamento:
1. configurar o serviço;
2. configurar variáveis de ambiente;
3. configurar PostgreSQL;
4. testar conexão;
5. executar migrações;
6. publicar;
7. testar login;
8. testar área administrativa;
9. testar uploads;
10. testar PWA.

## Histórico
O histórico oficial de cada publicação fica em `docs/12_DEPLOY.md`.
