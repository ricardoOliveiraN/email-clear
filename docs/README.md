# Documentação do email-clear

Este diretório concentra todas as decisões do projeto. A convenção é registrar o **o quê, o porquê, o como e o quando**.

## Como ler

| Pasta | Conteúdo | Quando consultar |
|-------|----------|------------------|
| `product/` | Visão, personas, funcionalidades (Free/Pago), glossário | Definir escopo, priorizar, alinhar produto |
| `decisions/` | ADRs (Architecture Decision Records): decisões aceitas, propostas e rascunhos | Antes de implementar algo novo ou mudar algo existente |
| `architecture/` | Visão arquitetural, componentes, diagramas | Entender o sistema como um todo |
| `planning/` | Estimativas de tempo, custos e aquisição de usuários | Planejamento de recursos e verba |
| `roadmap/` | Marcos (milestones) incrementais | Acompanhar progresso e próximos passos |
| `handoff/` | Estado atual, pendências e como retomar | Início/fim de cada sessão de trabalho |

## Fluxo de escrita

1. Contextualize na seção **Contexto**.
2. Documente a **Decisão** e o **Porquê** (alternativas descartadas).
3. Registre **Consequências** (positivas e negativas).
4. Sete o **Status** corretamente e o **Quando rever**.

### Status de um ADR

- `[Aceito]` — decisão tomada e vigente.
- `[Proposto]` — em validação; aguarda confirmação.
- `[Rascunho]` — ideia em discussão, ainda não decidida.
- `[Substituído por XXXX]` — não vigora mais; aponta a nova decisão.

## Convenção de numeração

ADRs e documentos usam prefixo numérico com zero à esquerda (`0001`, `0002`, …) para ordenação estável e referência cruzada.
