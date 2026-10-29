# ADR-0008: Votos de risco comunitário → lista de bloqueio

- **Status**: Proposto
- **Data**: 2026-08-31 (revisado em 2026-10-29)
- **Decisores**: time email-clear

## Contexto

Usuários podem marcar um remetente como perigoso (ou seguro). Após votos suficientes e confiáveis, o remetente ganha o título de **perigoso** e passa a influenciar o score ([ADR-0007](0007-classificacao-risco.md)). A mecânica de votação, thresholds e anti-abuso estavam em aberto.

## Decisão

### Escala

- **Binária**: `dangerous` / `safe`. Sem estrelas (simplicidade e menor ambiguidade).
- **1 voto por instalação por remetente** — deduplicação via `UNIQUE(instalacao_id, remetente_id)`.

### Threshold para o título "perigoso" (e "legítimo")

- **Limite inferior do intervalo de Wilson** (confiança **80%**, z=1,28) sobre a proporção de votos.
- Remetente vira **perigoso** quando `wilson_lower(votos_perigosos) > 0,7` **e** `total_votos >= 5`.
- Remetente vira **legítimo** quando `wilson_lower(votos_seguros) > 0,7` **e** `total_votos >= 5`.
- O mínimo de 5 votos evita que 1/1 (=100%) promova um remetente sozinho (anti-abuso).

### Contradição perigoso × legítimo

Impossível por construção: "perigoso" exige o limite inferior dos votos perigosos > 0,7 e "legítimo" exige o limite inferior dos votos seguros > 0,7. Como `perigosos + seguros = total`, os dois não podem ultrapassar 0,7 ao mesmo tempo. O remetente é **perigoso, legítimo ou indefinido** — nunca os dois.

### Anti-abuso

- Voto vinculado ao `install_id` (ADR-0005/0014); instalações forjadas são limitadas pela emissão de token por IP/sub-rede.
- Voto é **sinal, não verdade absoluta**: entra no score com peso de reputação — exceto quando atinge o título "perigoso", quando vira piso no ADR-0007.

### Transparência

- Expor contagem e proporção de votos no resultado (opcional; decisão de UI posterior).

### Pontos em aberto

- **Decay**: votos antigos (ex.: > 90 dias) perdem peso? Inicialmente **sem decay**; revisitar com dados.

## Consequências

Positivas:
- Robusto contra amostras pequenas e votos isolados.
- Simples de implementar e explicar.

Negativas:
- Requer volume de votos para surtir efeito (cold start da lista).
- Wilson + mínimo são heurísticas; precisam de calibração.

## Alternativas descartadas

- **Percentual puro (x% dos votos)**: 1/1 = 100% promove na hora (frágil).
- **Média simples com mínimo**: ainda sensível a votos extremos; Wilson é mais adequado.

## Quando rever

Com dados reais de votação: calibrar `wilson_lower` e `total_votos`, e decidir o decay.
