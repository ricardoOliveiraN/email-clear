# AGENTS.md

Guia para agentes de IA e contribuidores automatizados. Decisão registrada no [ADR-0012](docs/decisions/0012-convencoes-agentes.md).

## Mapa do repositório

| Caminho | Conteúdo |
|---------|----------|
| `docs/` | Documentação e decisões (ADRs). Consulte antes de mudar algo. |
| `extension/` | Extensão Chrome MV3 (TypeScript + Vite + CRXJS). Ver [ADR-0010](docs/decisions/0010-stack-extensao.md). |
| `backend/` | API FastAPI + worker (a criar — ver `docs/architecture/0002-estrutura-de-pastas.md`). |

## Comandos (executar em `extension/`)

- `npm install` — instala as dependências.
- `npm run dev` — Vite em watch; carregue `extension/dist` como extensão descompactada no Chrome.
- `npm run build` — typecheck + build de produção.
- `npm run typecheck` — `tsc --noEmit`.
- `npm run lint` — ESLint.
- `npm run format` — Prettier.
- `npm test` — Vitest.

## Regras de trabalho

1. Toda decisão nova ou alterada vira **ADR** em `docs/decisions/` e entra no índice (`docs/decisions/README.md`).
2. Consulte o ADR do assunto **antes** de implementar algo novo.
3. Atualize `docs/handoff/0001-estado-atual.md` ao fim da sessão.
4. Sem PII; segredos/chaves nunca no repositório (ver [ADR-0011](docs/decisions/0011-seguranca-cadeia-suprimentos.md)).
5. Dependências: manter `package-lock.json`, rodar `npm audit` e evitar pacotes com install scripts desconhecidos (ADR-0011).
