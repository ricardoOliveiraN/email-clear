# ADR-0008: Votos de risco comunitário → lista de bloqueio

- **Status**: Rascunho
- **Data**: 2026-08-31

## Contexto

Usuários podem atribuir uma nota de risco a um remetente (ex.: ao ver um destinário X, dar nota). Internamente, após uma quantidade X de votos, o remetente entra na lista de bloqueio. Detalhes de votação, thresholds e abuso estão em aberto.

## Perguntas em aberto

1. Escala da nota (aprovado/desaprovado, estrelas, 1–5)?
2. Quantos votos (X) e peso por voto para entrar na lista de bloqueio?
3. Como evitar votos abusivos/duplicados por instalação?
4. Idade/data do voto inflama (votos antigos contam)?
5. Impacto na lista de bloqueio: remeter decisão para todos os usuários ou só novos?
6. Transparência: mostrar contagem de votos ao usuário?

## Rascunho de decisão

- Voto vinculado ao UUID de instalação e à entidade (domínio/remetente), com deduplicação.
- Acima de um threshold ponderado por confiança (ex.: sinais de spam + votos), o remetente entra na lista de bloqueio.
- Notificar/refletir a decisão global nas validações (F01) e, no pago, mover para quarentena.

## Próximo passo

Definir escala, limites de votos e regras anti-abuso com o time.
