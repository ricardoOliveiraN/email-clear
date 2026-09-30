# Handoff — estado atual

Documento operacional para retomar o projeto sem reler tudo. **Atualizar a cada sessão** (novo arquivo `0002-...` ou revisão deste). Para planejamento, ver [`../roadmap/0001-marcos.md`](../roadmap/0001-marcos.md).

- **Data**: 2026-09-30 (fim de sessão)
- **Fase**: F1 — Fundação → **F2 (free, pré-backend)**. Extensão scaffolded, aviso (toast) e detecção por URL prontos; backend ainda não iniciado.
- **Branch**: `main` (mudanças **não commitadas**, prontas para commit — ver checklist)

## O que existe hoje

Documentação + **scaffold da extensão** (TypeScript + Vite + CRXJS, ADR-0010). Backend ainda não iniciado.

- `README.md` — descrição do produto e índice da documentação.
- `docs/product/` — visão, features (F01–F13), glossário.
- `docs/decisions/` — ADRs 0001–0016.
- `docs/architecture/` — visão arquitetural e estrutura de pastas.
- `docs/planning/` — estimativas de tempo/custo.
- `docs/roadmap/` — marcos F1–F6; F1 parcialmente concluída.
- `docs/handoff/` — este documento.
- `AGENTS.md` — comandos e regras para agentes (ADR-0012).
- `extension/` — extensão MV3 (scaffold funcional):
  - `src/background/service-worker.ts` — identidade + chamadas à API (evita CORS no MV3).
  - `src/content/content.ts` — observer do Gmail + orquestração (envia mensagem ao background).
  - `src/adapters/gmail/` — extração de remetente/assunto/corpo (seletores iniciais).
  - `src/core/` — `config`, `storage` (UUID/cache em `chrome.storage.local`), `api-client`, `mock` (temporário), `messaging`, `types`.
  - `src/ui/alert.ts` — aviso não-bloqueante no topo (toast) com Shadow DOM, cor por nível; fechável.

**Verificação**: `npm run typecheck`, `npm run lint`, `npm run build` e `npm test` passam; `npm audit` com **0 vulnerabilidades** (após subir `vite 8` e `vitest 5`, ADR-0011). **Smoke test confirmado**: alerta no topo aparece no Gmail com cor/nível corretos (modo mock); `MOCK_FORCE_LEVEL` em `config.ts` permite forçar um nível nos testes.

## Decisões consolidadas

| ADR | Tema | Status |
|-----|------|--------|
| 0001 | Arquitetura geral (extensão + backend + banco + filas) | Aceito |
| 0002 | Extensão Chrome MV3 / Gmail | Aceito |
| 0003 | Backend FastAPI | Aceito |
| 0004 | PostgreSQL | Aceito |
| 0005 | Identidade anônima e quota (modelo em camadas) | **Proposto** |
| 0006 | Injeção do aviso, quarentena e resiliência do adaptador | **Proposto** (fechado) |
| 0007 | Classificação e score de risco | **Rascunho** |
| 0008 | Votos comunitários → blocklist | **Rascunho** |
| 0009 | Pastas customizadas por conteúdo (cleaner) | **Rascunho** |
| 0010 | Stack da extensão (TS + Vite + Web Components) | Aceito |
| 0011 | Segurança da cadeia de suprimentos (dependências) | Aceito |
| 0012 | Convenções e comandos para agentes (AGENTS.md) | Aceito |
| 0013 | Gerenciador de pacotes — npm vs pnpm | **Rascunho** |
| 0014 | Token de instalação emitido pelo servidor | **Proposto** |
| 0015 | Cache em duas camadas e pré-checagem por hash de conteúdo | **Proposto** |
| 0016 | Configuração, segredos e armazenamento na extensão | **Proposto** |

## Pendências / blocos abertos

1. **ADR-0005 / ADR-0014** — identidade em camadas: UUID local (best-effort) + **token emitido pelo servidor** (HMAC), limites por IP/sub-rede, teto global, cache por mensagem e IA seletiva. Implementar no backend.
2. **ADR-0006** — fechado (Proposto). Implementar: alerta no topo para todos os níveis (base pronta em `src/ui/alert.ts`); botão de acionamento de quarentena (pago) via Gmail API; lote move já classificados **exceto lixeira**; estratégia de resiliência do adaptador (canário/telemetria anônima/testes de contrato); botão "marcar remetente como perigoso" no free.
3. **ADR-0007** — definir sinais, limiares de score (0–100 → faixas) e modelo de IA + custo por mensagem.
4. **ADR-0008** — definir escala de voto, thresholds e regras anti-abuso (fonte de votos no free: ADR-0006 §6).
5. **ADR-0009** — definir pastas customizadas/cleaner (F13).
6. **Diretório `backend/`** — ainda não criado (árvore em [`../architecture/0002-estrutura-de-pastas.md`](../architecture/0002-estrutura-de-pastas.md)).
7. **Adaptador Gmail** — `route.ts` já observa o hash (`hashchange`) e expõe `getThreadId` como chave estável; seletores de extração (`h2.hP`, `span.gD`, `div.a3s`) seguem frágeis; falta tratar threads com várias mensagens e `messageId` real para o cache.
8. **Modo mock ligado** — `USE_MOCK = true` em `src/core/config.ts`; desligar quando o backend existir.
9. **CI não configurado** — GitHub Actions (typecheck + lint + test + `npm audit`).
10. **Gerenciador de pacotes** — decidir npm vs pnpm (ADR-0013); hoje npm.
11. **Revisão/validação humana** — checklist abaixo; commit pendente.
12. **ADR-0015** — implementar cache L2 no servidor + pré-checagem por hash (`crypto.subtle` no cliente): definir TTL, normalização e eventual salt.
13. **ADR-0016** — migrar `API_BASE_URL` para `import.meta.env.VITE_API_BASE_URL`, derivar `USE_MOCK` de `import.meta.env.DEV` e garantir build de produção sem mock.

## Para commitar (sessão 2026-09-17)

Nada foi commitado ainda. Marque conforme validar.

**Criados**
- [ ] `AGENTS.md`, `.gitignore` (raiz)
- [ ] `docs/architecture/0002-estrutura-de-pastas.md`
- [ ] `docs/decisions/0009-pastas-customizadas-conteudo.md`
- [ ] `docs/decisions/0010-stack-extensao.md`
- [ ] `docs/decisions/0011-seguranca-cadeia-suprimentos.md`
- [ ] `docs/decisions/0012-convencoes-agentes.md`
- [ ] `docs/decisions/0013-gerenciador-pacotes-npm-pnpm.md`
- [ ] `docs/decisions/0014-identidade-servidor.md`
- [ ] `docs/decisions/0015-cache-duas-camadas-hash.md`
- [ ] `docs/decisions/0016-config-segredos-armazenamento.md`
- [ ] `docs/handoff/0001-estado-atual.md`
- [ ] `extension/` — configs (`manifest.json`, `vite.config.ts`, `tsconfig.json`, `eslint.config.js`, `.prettierrc.json`, `package.json`, `package-lock.json`, `.gitignore`) + `src/**`

**Alterados**
- [ ] `README.md`, `docs/README.md`, `docs/decisions/README.md`
- [ ] `docs/product/00-visao.md`, `01-features.md`, `02-glossario.md`
- [ ] `docs/planning/0001-estimativas.md`, `docs/roadmap/0001-marcos.md`
- [ ] `docs/decisions/0005-identidade-anonima-rate-limit.md` (revisado)
- [ ] `docs/decisions/0006-injecao-css-html-pastas.md` (revisado/fechado)
- [ ] `docs/decisions/0008-votos-risco-comunitario.md` (revisado)
- [ ] `docs/architecture/0001-visao-arquitetural.md`

> `extension/dist/` e `extension/node_modules/` estão no `.gitignore` — **não** entram no commit.

## Próxima sessão — pendências do free (pré-backend)

Fechado nesta sessão: ADR-0006 (aviso padrão = toast no topo, todos os níveis), ADR-0015 (cache em duas camadas), ADR-0016 (config/segredos/armazenamento) e detecção por URL (`adapters/gmail/route.ts`). O que falta **antes** de iniciar o backend:

**A. Extensão — endurecimento (maior risco)**
- [ ] **Adaptador Gmail**: tratar threads com **várias mensagens** (hoje `querySelector('.a3s.aiL')` pega a primeira) e capturar o **`messageId` real** (hoje `id: null`) para o cache.
- [ ] **Seletores com fallback em cascata** + degradação silenciosa (nunca aviso errado).
- [ ] **Observer estreito**: restringir o `MutationObserver` à raiz da conversa (hoje observa `document.body` inteiro).
- [ ] **Cache local**: chavear por `messageId` + TTL/limpeza (hoje por threadId, sem TTL).

**B. Testes e CI**
- [ ] **Vitest**: `route.ts` (`getThreadId`), `alert.ts`, `api-client.ts` e adaptador com **fixtures** do DOM do Gmail.
- [ ] **CI** (GitHub Actions): `npm ci` + typecheck + lint + test + `npm audit` (ADR-0011). Não configurado.

**C. Config/build (ADR-0016)**
- [ ] `API_BASE_URL` via `import.meta.env.VITE_API_BASE_URL` e `USE_MOCK` derivado de `import.meta.env.DEV`; garantir build de produção **sem mock**.

**D. UI/UX do free**
- [ ] Auto-dismiss do toast (opcional) e ícone por nível (hoje sempre `!`).
- [ ] Estado "validando…" (opcional) e decidir comportamento em falha de rede (hoje some em silêncio → avaliar "Não avaliado").

**E. Infra/prontidão**
- [ ] Decidir **npm vs pnpm** (ADR-0013); hoje npm.
- [ ] Ícones do manifest e revisão de permissões.

**F. Depois (depende do backend)**
- [ ] `backend/` + `/healthz`, depois `POST /v1/install` (ADR-0014) e `POST /v1/validate`; plugar `api-client`.
- [ ] Features F01/F02/F03/F06 e cache L2 + pré-check por hash (ADR-0015).

Ordem sugerida: **B → A → C → D → E → F.**


## Como retomar

1. `git status` e `git log --oneline -5` para confirmar o ponto de partida.
2. Ler este arquivo e o [roadmap](../roadmap/0001-marcos.md).
3. Consultar o ADR do assunto antes de implementar algo novo (índice em [`../decisions/README.md`](../decisions/README.md)).
4. Ao fim da sessão, atualizar este handoff (data, fase, checkboxes, novas decisões).

## Riscos conhecidos

- Mudanças no DOM do Gmail → custo de manutenção (F3+).
- Custo de IA no free → mitigar com quota (ADR-0005) e cache; estimar por mensagem (ADR-0007).
- Conversão free→pago incerta → validar valor percebido antes de F5.
