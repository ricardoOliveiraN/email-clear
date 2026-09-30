# Funcionalidades (Free vs Pago)

Backlog funcional. Prioridade: `P0` = MVP (testar), `P1` = próximo, `P2` = depois.

## Free (foco inicial — testes)

| ID | Funcionalidade | Descrição | Prioridade | Status |
|----|----------------|-----------|-----------|--------|
| F01 | Validação de remetente | Ao abrir o e-mail, consulta tabela de e-mails/domínios perigosos e conhecidos | P0 | Planejado |
| F02 | Validação de conteúdo | Detecção de phishing, engenharia social, links suspeitos, anexos | P0 | Planejado |
| F03 | Validação de e-mail suspeito | Heurísticas de reputação/comportamento do remetente | P0 | Planejado |
| F04 | Aviso via injeção | Injeção de CSS/HTML no webmail exibindo o resultado ao abrir o e-mail | P0 | Em andamento (mock) |
| F05 | Identidade anônima + quota | UUID de instalação para rate-limit sem login | P0 | Em andamento (UUID local; token do servidor pendente) |
| F06 | Armazenamento de decisões | Backend + PostgreSQL persistindo verificações e tabela de perigosos | P0 | Planejado |

## Pago (planejado — arquitetura já preparada)

| ID | Funcionalidade | Descrição | Prioridade | Status |
|----|----------------|-----------|-----------|--------|
| F07 | Processamento em lote via API | Varre em massa de e-mails pelos mesmos critérios, usando a API do serviço (Gmail API/OAuth) — não pela extensão | P1 | Rascunho |
| F08 | Classificação em lote | Classifica individualmente ou no lote | P1 | Rascunho |
| F09 | Pastas de organização | Movimentação para quarentena/outras pastas automaticamente | P1 | Rascunho |
| F10 | Filtros de automação | Regras por remetente/assunto/score | P2 | Rascunho |
| F13 | Pastas customizadas por conteúdo (cleaner) | Assinante cria pastas próprias; a classificação de conteúdo roteia e move as mensagens automaticamente, limpando a caixa de entrada (ADR-0009) | P1 | Rascunho |

> **F09 × F13 × F10**: F09 move **perigosos** para quarentena; F13 organiza **qualquer mensagem** em pastas definidas pelo assinante com base no **conteúdo**; F10 são filtros por regra (remetente/assunto/score). São complementares — a precedência entre elas é ponto em aberto no ADR-0009.

## Colaborativo (planejado)

| ID | Funcionalidade | Descrição | Prioridade | Status |
|----|----------------|-----------|-----------|--------|
| F11 | Nota de risco | Usuário atribui nota de risco a um remetente | P1 | Rascunho |
| F12 | Lista de bloqueio | Após X votos, remetente entra na lista de bloqueados | P1 | Rascunho |

## Fora de escopo agora

- Suporte a outros webmails (Gmail primeiro).
- App mobile ou produto standalone.
