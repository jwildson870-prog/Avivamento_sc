# Arquitetura Geral

## Stack definida
- Python
- Flask
- PostgreSQL
- Render
- GitHub
- Cloudflare
- Serviço de armazenamento de imagens, previsto como Cloudinary
- PWA

## O que não será usado
**Supabase não faz parte da arquitetura definida para este projeto.**

## Diagrama
```text
Usuário
  ↓
Domínio / Cloudflare
  ↓
Render
  ↓
Flask
  ├── PostgreSQL
  └── Armazenamento de imagens
```

## Regra de documentação
Quando qualquer serviço for trocado, este arquivo e o README específico do serviço devem ser atualizados.
