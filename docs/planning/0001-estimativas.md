# Estimativas

Projeções de tempo (aceleradas por IA), custos monetários e esforço de aquisição de usuários para o email-clear.

## Premissas

- **Disponibilidade: 2h/dia útil** (≈ 20 dias/mês → ~40h/mês).
- **Aceleração por IA**: grande parte do trabalho de código baseado em IA; estimamos tempo **com** uso intensivo de assistentes. Marcos possíveis de serem reduzidos ainda mais.
- Valores monetários são estimativas; confirmar com fornecedores/hosting antes de gastar.
- Custo de IA é a variável mais sensível — por isso a quota no free (ADR-0005) e a ponderação por mensagem (ADR-0007).

## Tempo (horas, com IA)

| Fase | Entrega | Horas estimadas | Sprints (2h/dia) |
|------|---------|-----------------|------------------|
| F1 — Fundação | Setup: repo, backend FastAPI + PostgreSQL, estrutura da extensão, CI local | ~12h | ~6 dias |
| F2 — Validação free | F01 remetente, F02 conteúdo, F03 suspeito, F04 aviso no Gmail, F05 quota | ~30h | ~15 dias |
| F3 — Robustez | Testes, tratamento de erro/DOM, cache, deploy (VPS/containers), seg. básica | ~24h | ~12 dias |
| F4 — Colaborativo | F11 nota de risco, F12 lista de bloqueio (thresholds, anti-abuso) | ~24h | ~12 dias |
| F5 — Pago (lote) | F07 processamento em lote, F08 classificação, F09 pastas/quarentena, workers | ~36h | ~18 dias |
| F6 — publicitário/Premium | Cobrança (planos), onboarding pago, métricas | ~40h | ~20 dias |

**Total declarado (com IA): ~166h** ≈ **~83 dias úteis** a 2h/dia (~4 meses). Sem IA, seria consideravelmente maior; assuma 2–4x.

> As fases variam conforme decisões em aberto (ADR-0006/0007/0008). Revisar após F2.

## Custo monetário (estimativas mensais)

| Item | Descrição | Custo estimado/mês |
|------|-----------|--------------------|
| VPS/hosting | Backend + worker (ex.: VPS de 4GB) | US$ 5–20 |
| Banco PostgreSQL | Hosted (ou na VPS) | US$ 0–15 |
| Domínio + TLS | Domínio próprio e certificado | US$ 1–3 |
| IA de classificação | Por requisição de validação de conteúdo | variável; controlar por quota |
| Chrome Web Store | Taxa de publicação (uma vez) | US$ 5 (único) |
| Monitoramento/logs | Observabilidade | US$ 0–10 |

**Total base (sem IA): ~US$ 10–35/mês.** O custo de IA é proporcional ao volume de mensagens validadas; estimar por mensagem antes (ADR-0007). Mitigação: quota free + cache + limitar IA a casos suspeitos.

## Esforço de aquisição de usuários

| Meta | Canal | Esforço | Observação |
|------|-------|---------|-----------|
| 10 usuários | Amigos/colegas/convidados diretos | Baixo | Beta manual (extensão + backend) |
| 100 usuários | Chrome Web Store (publicação) + comunidades de segurança/privacidade | Médio | Precisa de page/descrição icônos, capturas, FAQ |
| 1.000 usuários | Growth orgânico, SEO/landing, parceiros, rede social | Alto | Precisa de produto refiado + onboarding pago |

**Nota**: conseguir "usuários" grátis é barato; converter para **pagantes** é o desafio — o valor do lote/automação (F5) é o argumento de upsell.

## Marca-passos de verba

1. Se possível rodar na VPS mínima + domínio (~US$ 10/mês).
2. Só contratar plano de IA maior quando o volume validado indicar conversão.
3. Considerar cobrança/assinatura somente após F5 (lote) estar estável.

## Riscos de estimativa

- Mudanças frequentes no DOM do Gmail (custos de manutenção em F3+).
- Custo de IA não previsto no free → ajustar quota.
- Dificuldade de converter free→pago → atrasar F5 se o free não gerar valor percebido.
