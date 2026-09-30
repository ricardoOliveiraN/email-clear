# ADR-0009: Pastas customizadas por conteúdo (cleaner)

- **Status**: Rascunho
- **Data**: 2026-09-17

## Contexto

Além de proteger contra e-mails maliciosos, assinantes querem **limpar a caixa de entrada**: criar pastas próprias e fazer com que as mensagens sejam movidas automaticamente para elas com base no **conteúdo**. Diferente de F09 (quarentena de perigosos) e F10 (filtros por remetente/assunto/score), aqui o assinante define as pastas e o roteamento é orientado pela classificação de conteúdo.

Reaproveita a infraestrutura do plano pago: OAuth + Gmail API + worker de lote (ADR-0001). Restam decisões de produto e mecânica.

## Perguntas em aberto

1. **Quem define as pastas/regras**: o assinante (nome da pasta + critérios), sugestões automáticas por conteúdo, ou híbrido?
2. **Critérios de roteamento**: categoria de conteúdo, score, remetente/domínio, assunto? Combinação?
3. **Precedência**: o que vence entre F09 (quarentena), F13 (cleaner) e F10 (filtros)? Um e-mail pode ir para mais de uma pasta?
4. **Retroativo vs. novo**: mover só mensagens novas ou também o histórico (lote)?
5. **Limites por plano**: quantas pastas/regras por assinante.
6. **Falsos positivos**: como reverter (mover de volta) e evitar que mensagens legítimas sumam da entrada.
7. **Guardrails**: nunca mover remetentes confiáveis sem regra explícita; registrar toda movimentação para auditoria/undo.
8. **Escopos OAuth e cotas**: permissão de modificar (addLabel/removeLabel) e rate-limit da Gmail API.

## Rascunho de decisão

- O assinante cria **pastas** (labels Gmail, ex.: `email-clear/<nome>`) e associa **critérios** (conteúdo, score, remetente).
- O **worker** aplica as regras em lote via Gmail API (`addLabel`/`removeLabel`), reaproveitando a fila do ADR-0001.
- A classificação de conteúdo (ADR-0007) alimenta o roteamento; a decisão e a explicação são persistidas.
- Toda movimentação é **reversível** (undo) e não remove a mensagem, apenas troca a pasta.
- Quarentena (F09) tem **precedência** sobre o cleaner: perigosos nunca são roteados para pastas comuns.

## Consequências

Positivas:
- Valor claro de assinatura: caixa de entrada limpa e organizada sem trabalho manual.
- Reaproveita worker/OAuth do lote — baixo custo incremental.
- Aumenta o tempo de uso e a percepção de valor do plano pago.

Negativas:
- Mais escopo de privacidade: conteúdo é analisado no backend para rotear.
- Falsos positivos podem "esconder" mensagens importantes — exige undo e guardrails.
- Aumenta consumo de cotas da Gmail API e complexidade do worker.

## Alternativas descartadas

- **Filtros nativos do Gmail (só por remetente/assunto)**: não usa classificação de conteúdo, que é o diferencial.
- **Mover tudo no cliente (extensão)**: inviável para histórico e grandes volumes (limites do MV3, ADR-0001).
- **Pastas sugeridas sem controle do usuário**: menos flexível; mantém o "custom".

## Quando rever

Após validar os limites por plano e a taxa de falsos positivos do roteamento por conteúdo; ou se a precedência com F09/F10 gerar conflitos frequentes.
