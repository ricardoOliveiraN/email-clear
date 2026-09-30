# ADR-0015: Cache em duas camadas e pré-checagem por hash de conteúdo

- **Status**: Proposto
- **Data**: 2026-09-30
- **Decisores**: time email-clear

## Contexto

Validar cada mensagem aberta contra IA é caro e reenvia o conteúdo para o servidor a cada vez. O [ADR-0005](0005-identidade-anonima-rate-limit.md) já prevê "cache por mensagem — no cliente (por `messageId`/chave) e no servidor (por hash de conteúdo)", mas a mecânica não foi definida. Hoje o cliente envia o `OpenedEmail` inteiro em toda requisição (`extension/src/core/api-client.ts`) e o cache é só local, por `messageId` (`extension/src/core/storage.ts`).

Requisitos:
- Reduzir custo de IA e de rede (não revalidar a mesma mensagem para N instalações).
- Reduzir PII transmitida (idealmente, evitar enviar o corpo quando já houver resultado).
- Não confiar em campos forjáveis (remetente/assunto podem ser falsificados) como se fossem identidade confiável.

## Decisão proposta

Adotar **cache em duas camadas** com **pré-checagem por hash**:

1. **Camada L1 — cliente** (`chrome.storage.local`, por `messageId`): já existe; responde offline e evita viagens repetidas.
2. **Camada L2 — servidor** (por **hash de conteúdo**): normaliza-se a tupla `remetente + assunto + corpo` (remover espaços/quotes redundantes) e calcula-se `SHA-256`. O resultado da classificação é armazenado com TTL.
3. **Pré-checagem (miss/hit)**: o cliente calcula o hash **localmente** (`crypto.subtle`) e envia **apenas o hash** (ex.: `POST /v1/validate/lookup`). Em *hit*, o servidor devolve a classificação sem pedir o conteúdo; em *miss*, o cliente envia o conteúdo completo para análise (`POST /v1/validate`), e o servidor computa/armazena o mesmo hash.
4. **Só IA acima do limiar heurístico** (ADR-0007): o cache só precisa cobrir o estágio que usa IA; heurísticas baratas podem rodar sempre.
5. **Poisoning**: como remetente/assunto são forjáveis, o cache **não** é tratado como "seguro por decreto": usar TTL curto, escopo por confiança e nunca servir cache como sinal forte isolado; heurísticas de segurança sempre reavaliadas.
6. **Privacidade do hash**: o hash é determinístico e derivado de conteúdo em grande parte público; avaliar **salt** (servidor) e rotação para evitar correlação entre usuários e precomputação. Ponto aberto para o backend.

## Consequências

Positivas:
- Custo de IA e latência caem de forma significativa (mensagens repetidas e campanhas em massa viram *hit*).
- Menos PII trafegando: em *hit*, só o hash sai do cliente.
- Serve N instalações a partir de um único cálculo por conteúdo.

Negativas:
- Mais complexidade: dois endpoints, normalização estável e política de TTL/invalidação.
- Risco de envenenamento do cache por conteúdo forjado (mitigado por TTL/escopo/heurísticas).
- Fragilidade da normalização: pequenas diferenças geram hashes distintos (perda de *hit*), não incorreção.
- Requer backend para L2 (funciona degradado só com L1 enquanto não existir).

## Alternativas descartadas

- **Só cache local (L1)**: cada instalação revalida conteúdo repetido; custo de IA escala com o número de instalações.
- **Cache global por remetente/título apenas**: colide demais (newsletters, assuntos genéricos) e é trivialmente forjável.
- **Enviar sempre o conteúdo completo**: maior custo e mais PII trafegada; desperdiça o potencial de deduplicação.
- **Cachear e servir sem reavaliar heurísticas**: abre envenenamento (remetente spoofado com resultado "seguro").

## Quando rever

Ao implementar o backend (F1/F2), ao definir TTL/normalização e ao medir a taxa de *hit* real. Reavaliar a necessidade de salt se houver tentativa de correlação entre usuários.
