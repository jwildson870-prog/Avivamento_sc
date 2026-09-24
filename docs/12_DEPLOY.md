# Deploy — Histórico Permanente

Este arquivo é o diário de deploys do projeto.

## Ambiente atual
- Aplicação: Flask/Python
- Servidor: Render
- Banco: PostgreSQL
- Código: GitHub
- DNS/HTTPS: Cloudflare
- Armazenamento de imagens: Cloudinary (quando configurado)
- PWA: habilitado conforme a implementação atual

## Como registrar um novo deploy

Depois de cada deploy, adicione uma entrada no topo do histórico usando este modelo:

```markdown
## Deploy #001 — AAAA-MM-DD
- Commit:
- Branch:
- Ambiente: produção
- Alterações:
  - 
  - 
- Banco/migrações:
  - 
- PWA:
  - 
- Testes realizados:
  - 
- Resultado:
- Observações:
```

## Histórico

### Deploy #001 — Inicial
- Status: projeto inicial/documentação criada.
- Observação: substituir esta entrada pelos dados reais quando o primeiro deploy de produção acontecer.

## Regra
**Nunca apagar deploys antigos.** Cada novo deploy deve ser acrescentado ao histórico. Isso permite acompanhar a evolução do site e descobrir o que mudou em cada publicação.
