# Handoff — estado atual

Documento operacional para retomar o projeto sem reler tudo. **Atualizar a cada sessão** (novo arquivo `0002-...` ou revisão deste). Para planejamento, ver [`../roadmap/0001-marcos.md`](../roadmap/0001-marcos.md).

- **Data**: 2026-10-29 (fim de sessão)
- **Fase**: F1 — Fundação (**backend iniciado**). Extensão F2 (free) pronta em modo mock; backend com `/v1/healthz` + modelos de dados criados — **ainda sem** endpoints de instalação/validação/voto.
- **Branch**: `main` (mudanças **não commitadas** — ver checklist)

## O que existe hoje

Documentação + **extensão (scaffold funcional, mock)** + **backend inicial** (FastAPI + PostgreSQL + Alembic).

- `README.md`, `docs/product/`, `docs/decisions/` (ADRs 0001–0016), `docs/architecture/`, `docs/planning/`, `docs/roadmap/`, `AGENTS.md`.
- `extension/` — MV3 (TS + Vite + CRXJS): toast de aviso (Shadow DOM) com **botões de voto** ("Perigoso" / "Legítimo"), detecção por URL. **Plugada ao backend**: `API_BASE_URL` via `import.meta.env.VITE_API_BASE_URL` (default `http://127.0.0.1:8000`), token de instalação via `POST /v1/install` (ADR-0014); mock só com `VITE_USE_MOCK=true`.
- `backend/` — (ADR-0003/0004):
  - `app/main.py` — FastAPI.
  - `app/api/v1/` — `GET /v1/healthz`; `POST /v1/install` (token HMAC, ADR-0014); `POST /v1/validate/lookup` (cache L2, ADR-0015); `POST /v1/validate` (remetente → links → conteúdo, ADR-0007); `POST /v1/vote` (voto perigoso/legítimo, ADR-0008).
  - `app/core/` — `config.py` (pydantic-settings) + `security.py` (token HMAC).
  - `app/db/` — engine/sessão async (SQLAlchemy 2 + asyncpg).
  - `app/models/` — `instalacao`, `remetente`, `voto_remetente`, `link`, `verificacao_link`, `classificacao`.
  - `app/domain/` — `normalize` (hash/URL), `score` (Wilson bidirecional + faixas + desconto de legítimo), `heuristics` (fallback sem IA).
  - `app/services/` — `ai` (OpenRouter), `safebrowsing`, `links`, `remetentes` — atrás de interfaces mockáveis.
  - `alembic/` — migration inicial aplicada.
  - `tests/` — 22 testes (health, domain, security).
- `docker-compose.yml` (raiz) — `db` (Postgres 16) + `backend` (roda `alembic upgrade head` e sobe o uvicorn).

**Verificação**: `docker compose up -d --build` sobe tudo; `GET /v1/healthz` → `{"status":"ok","database":"ok"}`. Fluxo testado: `install` → `validate` → `lookup` (hit) → `vote` (5 votos → remetente `legitimate`/`dangerous`, com desconto/piso no score). `cd backend && .venv/Scripts/python -m pytest` = 22 passed; `ruff check` limpo.

## Comandos

- Extensão: `cd extension` → `npm run dev|build|typecheck|lint|test`.
- Backend (docker): `docker compose up -d --build` (db + api); `docker compose logs -f backend`.
- Backend (local, venv): `cd backend` → `.venv/Scripts/python -m alembic upgrade head` / `.venv/Scripts/python -m pytest` / `.venv/Scripts/python -m ruff check app`.

## Decisões consolidadas

| ADR | Tema | Status |
|-----|------|--------|
| 0001 | Arquitetura geral (extensão + backend + banco + filas) | Aceito |
| 0002 | Extensão Chrome MV3 / Gmail | Aceito |
| 0003 | Backend FastAPI | Aceito |
| 0004 | PostgreSQL | Aceito |
| 0005 | Identidade anônima e quota (modelo em camadas) | **Proposto** |
| 0006 | Injeção do aviso, quarentena e resiliência do adaptador | **Proposto** (fechado) |
| 0007 | Classificação e score de risco | **Proposto** (revisado — sinais/pesos/faixas fixados) |
| 0008 | Votos comunitários → blocklist | **Proposto** (revisado — Wilson bidirecional: perigoso **e** legítimo) |
| 0009 | Pastas customizadas por conteúdo (cleaner) | **Rascunho** |
| 0010 | Stack da extensão (TS + Vite + Web Components) | Aceito |
| 0011 | Segurança da cadeia de suprimentos (dependências) | Aceito |
| 0012 | Convenções e comandos para agentes (AGENTS.md) | Aceito |
| 0013 | Gerenciador de pacotes — npm vs pnpm | **Rascunho** |
| 0014 | Token de instalação emitido pelo servidor | **Proposto** |
| 0015 | Cache em duas camadas e pré-checagem por hash de conteúdo | **Proposto** |
| 0016 | Configuração, segredos e armazenamento na extensão | **Proposto** |

## Pendências / blocos abertos

**A. Backend — o que falta (em ordem)**
- [x] `POST /v1/install` — token HMAC (ADR-0014), rate-limit por IP (em memória).
- [x] `POST /v1/validate/lookup` — pré-checagem por hash (ADR-0015).
- [x] `POST /v1/validate` — remetente (votos) → links (Safe Browsing) → conteúdo (OpenRouter/heurística).
- [x] `domain/` (score/Wilson/normalização) e `services/` (OpenRouter/Safe Browsing/links/remetentes), atrás de interfaces mockáveis.
- [x] `POST /v1/vote` — voto perigoso/legítimo com dedup + Wilson bidirecional (ADR-0008).
- [x] **Remetente legítimo** — 5+ votos "safe" → desconto de 50% no risco de conteúdo (ADR-0007/0008).
- [x] **UI de voto** na extensão (botões "Perigoso"/"Legítimo" no toast).
- [ ] Rate-limit/quota compartilhados (hoje em memória; produção → Redis) e limites por sub-rede.
- [ ] Testes de integração dos endpoints (hoje: 22 testes unitários).

**B. Extensão — endurecimento (maior risco, pré-backend)**
- [ ] **Adaptador Gmail**: threads com várias mensagens + `messageId` real (hoje `id: null`).
- [ ] Seletores com fallback em cascata + degradação silenciosa.
- [ ] Observer estreito (raiz da conversa, não `document.body`).
- [ ] Cache local por `messageId` + TTL/limpeza.

**C. Testes e CI**
- [ ] Vitest: `route.ts`, `alert.ts`, `api-client.ts`, adaptador com fixtures do DOM.
- [ ] CI (GitHub Actions): backend (ruff + pytest) e extensão (typecheck + lint + test + `npm audit`).

**D. Config/build (ADR-0016)**
- [x] `API_BASE_URL` via `import.meta.env.VITE_API_BASE_URL`; `USE_MOCK` via `VITE_USE_MOCK` (off por padrão); token de instalação plugado (`api-client` + `storage`).

**E. UI/UX do free**
- [ ] Auto-dismiss do toast + ícone por nível.
- [ ] Estado "validando…" e comportamento em falha de rede.
- [ ] Popup (`action.default_popup`) e Options (`options_ui`).

**F. Infra/prontidão**
- [ ] Decidir npm vs pnpm (ADR-0013).
- [ ] Ícones do manifest e revisão de permissões.

## Para commitar (sessão 2026-10-29)

Nada foi commitado ainda nesta sessão. Marque conforme validar.

**Criados**
- [ ] `backend/` — `pyproject.toml`, `Dockerfile`, `.dockerignore`, `.env.example`, `.gitignore`, `alembic.ini`, `alembic/**`, `app/**` (core/db/models/api/schemas/domain/services/main), `tests/**`
- [ ] `docker-compose.yml` (raiz)
- [ ] `.env.example` (raiz)

**Alterados**
- [ ] `.gitignore` (raiz — entradas Python + `!.env.example`)
- [ ] `extension/` — `manifest.json`, `src/core/{config,storage,api-client,messaging,types}.ts`, `src/background/service-worker.ts`, `src/content/content.ts`, `src/ui/alert.ts` + `.env.example`
- [ ] `docs/decisions/0007-classificacao-risco.md` (revisado → Proposto)
- [ ] `docs/decisions/0008-votos-risco-comunitario.md` (revisado → Proposto)
- [ ] `docs/decisions/README.md` (status 0007/0008)
- [ ] `docs/roadmap/0001-marcos.md` (F1: backend + PostgreSQL marcados)
- [ ] `docs/handoff/0001-estado-atual.md` (este arquivo)

> `backend/.venv/`, `__pycache__/` e `backend/.env` estão no `.gitignore` — **não** entram no commit.

## Como retomar

1. `git status` e `git log --oneline -5` para confirmar o ponto de partida.
2. Ler este arquivo e o [roadmap](../roadmap/0001-marcos.md).
3. Consultar o ADR do assunto antes de implementar algo novo (índice em [`../decisions/README.md`](../decisions/README.md)).
4. Ao fim da sessão, atualizar este handoff (data, fase, checkboxes, novas decisões).

## Riscos conhecidos

- Mudanças no DOM do Gmail → custo de manutenção (F3+).
- Custo de IA no free → mitigar com quota (ADR-0005) e cache por hash (ADR-0015); estimar por mensagem (ADR-0007).
- Conversão free→pago incerta → validar valor percebido antes de F5.
- **OpenRouter/Safe Browsing** são serviços externos com custo e chave de API — sem chave, os endpoints de validação terão que degradar para heurísticas (a definir).
