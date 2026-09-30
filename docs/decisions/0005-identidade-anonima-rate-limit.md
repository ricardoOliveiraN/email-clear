# ADR-0005: Identidade anônima e quota sem login

- **Status**: Proposto
- **Data**: 2026-08-31 (revisado em 2026-09-17)
- **Decisores**: time email-clear

## Contexto

A validação ao abrir e-mail deve funcionar no **free tier sem exigir conta**. Isso cria a dúvida de como limitar o uso de requisições (e o custo de IA) por usuário/instalação sem login.

Requisitos:
- Não coletar PII.
- Aplicar quota por "usuário" (instalação/device).
- Não servir como autenticação de segurança.
- Limitar abuso (muitas requisições).

**Premissa revisada**: identidade gerada no cliente **não é confiável**. Qualquer valor gerado/armazenado no cliente pode ser alterado. Portanto, o identificador de instalação é apenas uma **contabilidade best-effort**, nunca autorização.

## Decisão proposta

Adotar um modelo **em camadas**, assumindo cliente hostil:

1. **UUID de instalação local** — gerado na primeira execução e persistido em **`chrome.storage.local`** (storage da extensão; **não** `localStorage`, que é do Gmail, nem cookie). É anônimo, sem PII e serve só para contabilidade/UX offline. **Não é credencial.**
2. **Token de instalação emitido pelo servidor** ([ADR-0014](0014-identidade-servidor.md)) — a barreira real contra forja. O backend emite e valida o token; o segredo fica no servidor.
3. **Limites por IP/sub-rede + teto global diário** — o que efetivamente contém o custo, independente do cliente.
4. **Cache por mensagem** — no cliente (por `messageId`/chave) e no servidor (por hash de conteúdo), evitando revalidar a mesma mensagem para N instalações.
5. **IA só acima de limiar heurístico** (ADR-0007) — a maioria das requisições fica barata; abuso deixa de compensar.
6. **Hash do UUID no banco** — medida de **privacidade** (não vaza vínculo em caso de vazamento), **não** de anti-abuso.

Permanece **sem login** no free; login é opcional (sincronizar/upgrade).

## Consequências

Positivas:
- Free tier funcional e sem atrito (funciona offline com o UUID local; registra o token quando online).
- Custo de IA contido por limites de servidor, não por confiança no cliente.
- Base para migrar à conta paga depois.

Negativas:
- UUID local é forjável — mitigado pelas camadas 2–5.
- Requer backend na primeira emissão de token (fallback: quota mínima enquanto não registrar).
- Mais peças para operar (emissão, expiração/rotação, limites por IP).

## Alternativas descartadas

- **Chave secreta embutida na extensão para assinar o UUID**: a chave é distribuível/desempacotável — não é segredo. Obscuridade, não segurança.
- **Confiar só no UUID**: forjável; trocar o valor = nova quota.
- **Somente IP**: não confiável (NAT, proxies) e penaliza usuários legítimos.
- **API key por download**: vaza no pacote.
- **Conta obrigatória**: fere o requisito de "sem login" no free.
- **`localStorage`/cookie para o UUID**: `localStorage` do content script pertence ao Gmail; cookie é mecanismo de sessão e seria enviado ao webmail.

## Quando rever

Se a falsificação de UUID gerar abuso relevante, ou se o login se tornar default. Validar o modelo de token (ADR-0014) com o time antes de implementar o rate-limit em produção.
