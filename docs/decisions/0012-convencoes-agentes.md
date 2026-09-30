# ADR-0012: Convenções e comandos para agentes (AGENTS.md)

- **Status**: Aceito
- **Data**: 2026-09-17
- **Decisores**: time email-clear

## Contexto

O projeto é escrito com apoio de agentes de IA (opencode) em sessões intercaladas. Sem um ponto único que diga **como construir, testar e lintar**, cada sessão redescobre comandos ou usa "atalhos" errados. Também é preciso reforçar o fluxo de decisão (consultar/registrar ADR) e onde está o estado atual.

## Decisão

Manter um arquivo **`AGENTS.md` na raiz** com:

1. **Mapa do repositório** (`docs/`, `extension/`, `backend/`).
2. **Comandos por pacote** — em `extension/`: `npm install`, `npm run dev`, `npm run build`, `npm run typecheck`, `npm run lint`, `npm run format`, `npm test`.
3. **Regras de trabalho**:
   - Toda decisão nova/alterada vira **ADR** em `docs/decisions/` (e entra no índice).
   - Consultar o ADR do assunto **antes** de implementar.
   - Atualizar `docs/handoff/0001-estado-atual.md` ao fim da sessão.
   - Sem PII; segredos nunca no repositório (ADR-0011).

**Por quê**: dar contexto durável ao agente, padronizar comandos e preservar as decisões entre sessões.

## Consequências

Positivas:
- Onboarding imediato de agentes e pessoas; menos erro de comando.
- Reforça a cultura de ADR e de handoff (rastreabilidade).
- Comandos centralizados em vez de espalhados em conversas.

Negativas:
- Mais um documento para **manter atualizado**; se os scripts mudarem sem atualizar, vira fonte de erro.
- Pode duplicar informação do `README`/`docs` (mitigar mantendo o `AGENTS.md` enxuto e referenciando os ADRs).

## Alternativas descartadas

- **Documentar só no `README`**: mistura "como usar o produto" com "como contribuir/agir".
- **`CONTRIBUTING.md` apenas**: foco humano; agents precisam do arquivo convencionado (`AGENTS.md`) para serem lidos automaticamente.
- **Nada**: cada sessão recomeça a instrução — foi o problema observado.

## Quando rever

Se o repositório ganhar múltiplos pacotes com fluxos distintos (backend) e o `AGENTS.md` ficar grande, dividir em `AGENTS.md` por pacote referenciando o da raiz.
