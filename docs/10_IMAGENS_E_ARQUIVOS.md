# Imagens e Arquivos

## Tipos
O projeto pode trabalhar com:
- foto de perfil;
- foto de pastor;
- imagem institucional;
- ícones do PWA.

## Armazenamento
A arquitetura definida prevê um serviço de armazenamento de imagens, como Cloudinary, em vez de depender do disco temporário do servidor.

## Fluxo
```text
Usuário
→ Flask
→ armazenamento de imagens
→ URL/referência
→ PostgreSQL
```

## Regras
- Validar tipo e tamanho do arquivo.
- Não confiar somente na extensão.
- Não armazenar segredos dentro das imagens.
- Registrar mudanças importantes neste documento.
