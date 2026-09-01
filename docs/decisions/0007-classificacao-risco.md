# ADR-0007: Classificação e score de risco

- **Status**: Rascunho
- **Data**: 2026-08-31

## Contexto

O email-clear precisa atribuir uma classificação às mensagens (individual ou em lote) a partir da validação de remetente, de conteúdo (phishing, engenharia social, links, anexos) e de suspeita. A mecânica do score e os limiares estão em aberto.

## Perguntas em aberto

1. Como combinar os sinais (remetente, conteúdo, links, anexos) em um score único?
2. Quais limiares definem "seguro / suspeito / perigoso"?
3. Uso de modelo de IA para conteúdo: qual modelo, como orquestrar com heurísticas (custo)?
4. Como ponderar o custo de IA por mensagem vs. precisão?
5. Feedback do usuário ajusta os modelos/limiares?

## Rascunho de decisão

- Combinar heurísticas determinísticas (listas, padrões de phishing, reputation de domínio) com análise de IA do conteúdo.
- Gerar score normalizado (ex.: 0–100) e mapear a faixas de classificação.
- Persistir score, sinais disparados e a explicação (para transparência).

## Próximo passo

Definir os sinais e limiares iniciais, escolher o modelo de IA e estimar custo por mensagem (ver `planning/0001-estimativas.md`).
