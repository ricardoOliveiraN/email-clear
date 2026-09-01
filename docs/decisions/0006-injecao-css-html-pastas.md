# ADR-0006: Injeção CSS/HTML e pastas (quarentena)

- **Status**: Rascunho
- **Data**: 2026-08-31

## Contexto

A extensão precisa comunicar o resultado ao usuário (aviso visual ao abrir o e-mail) e, no plano pago, organizar e-mails perigosos movendo-os para pastas (ex.: quarentena). Ainda não há decisão sobre a mecânica exata (pontos de inserção, granularidade do aviso, criação/movimentação de pastas no webmail).

## Perguntas em aberto

1. Onde exatamente injetar o aviso (banner no topo, card ao lado do e-mail, badge na lista)?
2. Qual o comportamento no free: só aviso, ou também pastas básicas?
3. Como criar/mover pastas: prefere-se via **API com autenticação (Gmail API/OAuth)**, dado que o lote já será via API (ADR-0001); validar escopo/permissoes.
4. O que acontece com e-mails já classificados (marcação persistente ou só visual)?
5. Tratamento de erros quando o DOM/Gmail mudar.

## Rascunho de decisão

- Injetar aviso via content script ao detectar abertura de e-mail, usando CSS de baixa intrusão.
- No pago, criar label "email-clear/quarentena" e mover e-mails classificados como perigosos.
- Cachear resultado (id da mensagem) para não revalidar a cada abertura.

## Próximo passo

Validar os pontos acima com o time e preencher decisão, consequências e alternativas.
