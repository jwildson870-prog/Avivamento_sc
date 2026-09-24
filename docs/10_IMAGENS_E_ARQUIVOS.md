# Imagens e arquivos

## Armazenamento

As fotos de perfil e dos pastores usam **Backblaze B2** em produção. O bucket configurado para o projeto é `Avivamento`.

Variáveis no Render:
- `B2_KEY_ID` — ID da chave de aplicação.
- `B2_APPLICATION_KEY` — chave secreta.
- `B2_BUCKET_NAME=Avivamento`.
- `B2_ENDPOINT_URL=https://s3.us-east-005.backblazeb2.com`.
- `B2_REGION=us-east-005`.

O bucket pode permanecer privado. O aplicativo gera URLs temporárias assinadas para exibir as imagens.

Sem credenciais B2, o sistema usa `app/static/uploads/` localmente.
