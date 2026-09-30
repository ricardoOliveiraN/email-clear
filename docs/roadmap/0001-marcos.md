# Roadmap / Marcos

Progresso incremental. O foco de implementação começa no **Free** (para testes) mesmo com o MVP contemplando tudo. Arquiteto pronto para o pago.

## Fase F1 — Fundação
**Objetivo**: esqueleto funcional para começar.

- [x] Estrutura da extensão `extension/` (TypeScript + Vite + CRXJS — ADR-0010)
- [x] Esqueleto da extensão Chrome MV3 + adaptador Gmail (stub)
- [ ] Estrutura do backend `backend/` + FastAPI rodando (endpoint saúde)
- [ ] PostgreSQL local (docker) + modelos básicos (remetentes perigosos, verificações)
- [ ] CI local (lint/testes) e docker-compose de dev

## Fase F2 — Validação Free (MVP de testes)
**Objetivo**: validar e-mails ao abrir no Gmail e avisar o usuário.

- [ ] F01 — tabela de e-mails/domínios perigosos + lookup
- [ ] F02 — validação de conteúdo (phishing, engenharia social, links, anexos)
- [ ] F03 — heurísticas de e-mail suspeito (reputação/comportamento)
- [ ] F04 — injeção do aviso (CSS/HTML) ao abrir e-mail
- [ ] F05 — UUID de instalação + quota/rate-limit (ADR-0005)
- [ ] F06 — persistência de decisões e resultados

**Saída esperada**: abrir um e-mail malicioso no Gmail → aviso do email-clear funcionando.

## Fase F3 — Robustez
**Objetivo**: confiar no free tier.

- [ ] Testes de regras e de adaptador Gmail; tratamento de erro de rede/DOM
- [ ] Cache de resultados por mensagem (evitar revalidação)
- [ ] Deploy (VPS/containers), logs, monitoramento, backup
- [ ] Segurança básica (headers, hash de UUID, rate-limit)

## Fase F4 — Colaborativo
**Objetivo**: proteger coletivamente.

- [ ] F11 — atribuição de nota de risco pelo usuário
- [ ] F12 — lista de bloqueio por votos (thresholds + anti-abuso) (ADR-0008)

## Fase F5 — Pago (lote + automação via API)
**Objetivo**: valor ao plano premium.

- [ ] OAuth + tokens de acesso ao e-mail (Gmail API) no backend
- [ ] F07 — processamento em lote via Gmail API (listagem paginada + backoff/cotas)
- [ ] F08 — classificação em lote
- [ ] F09 — pastas/quarentena automáticas (addLabel via API) (ADR-0006)
- [ ] F10 — filtros/automação por regra
- [ ] F13 — pastas customizadas por conteúdo (cleaner): roteamento por regra + classificação (ADR-0009)

## Fase F6 — Produto/Premium
**Objetivo**: converter e distribuir.

- [ ] Robust/métricas de uso e conversão
- [ ] Cobrança/planos (assinatura)
- [ ] Onboarding pago, página de marketing, Release na Chrome Web Store
- [ ] Suporte a outros webmails (segundo serviço)

## Critérios de avanço de fase

Avançar quando a fase atual estiver estável (testes passando) e com valor percebido, não apenas "código rodando".
