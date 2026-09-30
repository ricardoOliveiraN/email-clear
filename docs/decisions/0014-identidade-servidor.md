# ADR-0014: Token de instalação emitido pelo servidor

- **Status**: Proposto
- **Data**: 2026-09-17
- **Decisores**: time email-clear

## Contexto

O ADR-0005 define um UUID local anônimo para quota, mas ele é **forjável**: quem quiser burlar troca o valor e ganha quota nova. Assinar no cliente não resolve (a chave estaria no pacote da extensão, que é distribuível). Precisamos de uma barreira **verificável pelo servidor** sem exigir login.

## Decisão proposta

Adotar um **token de instalação emitido pelo servidor**:

1. Na primeira execução **online**, a extensão chama `POST /v1/install`.
2. O backend cria um `install_id` aleatório e devolve um **token assinado** — modelo simples: `token = install_id + '.' + HMAC(segredo_servidor, install_id)`. O segredo **nunca** sai do servidor.
3. A extensão guarda `install_id` + `token` em `chrome.storage.local`.
4. Toda requisição de validação envia o token (ex.: header `X-Install-Token`). O backend **valida a assinatura** e aplica quota por `install_id`.
5. O endpoint `POST /v1/install` é **limitado por IP/sub-rede e por dia** (senão o atacante emite IDs legítimos em massa).
6. **Fallback offline**: sem token (primeira execução sem rede), a extensão usa o UUID local e recebe uma **quota mínima**; ao ficar online, registra e passa ao token.
7. **Expiração/rotação**: tokens têm validade; renovação via `POST /v1/install/refresh` (também limitado).

Isto **complementa** as outras camadas do ADR-0005 (limites por IP, cache por mensagem, IA seletiva).

## Consequências

Positivas:
- Eleve a barra: forjar exige obter token de um servidor que limita a emissão por IP/dia.
- O servidor deixa de confiar cegamente no cliente para contabilizar uso.
- Segredos ficam só no servidor (nada sensível no pacote).

Negativas:
- Depende de rede para o primeiro registro (mitigado pelo fallback offline com quota mínima).
- Mais complexidade: emissão, validação HMAC, expiração, limites de emissão.
- Estado no servidor por instalação (armazenar `install_id` + hash; nunca PII).
- Contorna-se com muitas IPs (bots) — daí os limites por sub-rede e o teto global.

## Alternativas descartadas

- **UUID puro** (ADR-0005 original): forjável, sem barreira.
- **Chave secreta na extensão**: extraível; não é segredo.
- **JWT autoassinado pelo cliente**: sem segredo no cliente, não há como assinar.
- **OAuth/conta obrigatória**: contraria o "free sem login".
- **mTLS/attestation de dispositivo**: não disponível de forma genérica para extensões de navegador.

## Quando rever

Ao implementar o backend (F1/F2) e definir os limites de emissão e a validade do token. Reavaliar se aparecer abuso por emissão massiva (muitas IPs) ou se o fallback offline for explorado.
