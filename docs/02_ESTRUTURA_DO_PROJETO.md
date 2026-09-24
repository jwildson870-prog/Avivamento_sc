# Estrutura do Projeto

## Organização
O projeto é dividido em aplicação Python/Flask, templates, arquivos estáticos, documentação e configuração.

```text
avivamento_site/
├── app/
│   ├── templates/
│   └── static/
├── docs/
├── requirements.txt
├── README.md
└── arquivos de configuração
```

## Princípios
- Rotas e regras de negócio ficam no backend.
- HTML fica nos templates.
- CSS e JavaScript ficam nos arquivos estáticos.
- Documentação técnica fica em `docs/`.
- Segredos não devem ser versionados.

## Regra de manutenção
Toda mudança estrutural relevante deve atualizar este documento e o README específico afetado.
