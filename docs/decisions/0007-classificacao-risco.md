# ADR-0007: Classificação e score de risco

- **Status**: Proposto
- **Data**: 2026-08-31 (revisado em 2026-10-29)
- **Decisores**: time email-clear

## Contexto

O email-clear precisa atribuir uma classificação às mensagens a partir de sinais: reputação do remetente (votos — [ADR-0008](0008-votos-risco-comunitario.md)), conteúdo (phishing/engenharia social via IA) e links suspeitos. A mecânica do score e os limiares estavam em aberto; esta revisão os fixa (valores iniciais, calibráveis).

## Decisão

Combinar três sinais em um **score único 0–100**, com **pisos (overrides)** determinísticos para casos de alta confiança.

### Sinais e pesos (provisórios)

| Sinal | Fonte | Peso |
|-------|-------|------|
| Reputação do remetente | votos comunitários (ADR-0008) + listas | 0–20 |
| Conteúdo (phishing, engenharia social, urgência, impersonação) | IA (OpenRouter), saída JSON estruturada | 0–70 |
| Links suspeitos | Google Safe Browsing (principal) + IA (contexto/fallback) | 0–10 |

`score = min(100, soma(pesos))`.

> **Conteúdo é o sinal dominante** no free (sem login/votos prévios nem blocklist de links, o conteúdo precisa conseguir sair de "seguro" sozinho). A IA devolve `phishing_score` em **0–100** e o componente de conteúdo o pondera para 0–70.

### Pisos e descontos (overrides)

- Remetente classificado **perigoso** por votos (ADR-0008) → `score = max(score, 80)`.
- Remetente classificado **legítimo** por votos (ADR-0008) → conteúdo × 0,5 (remetente confiável reduz o risco do conteúdo).
- Link em **blocklist do Safe Browsing** (`MALWARE` / `SOCIAL_ENGINEERING`) → `score = max(score, 85)`.

### Faixas de classificação

| Score | Nível |
|-------|-------|
| 0–39 | `safe` |
| 40–69 | `suspicious` |
| 70–100 | `dangerous` |

### IA (conteúdo)

- Provedor: **OpenRouter** (permite trocar de modelo sem refatorar o orquestrador).
- Saída **JSON estruturado** (não texto livre): `phishing_score` (0–100), indicadores (urgência, impersonação, links suspeitos, engenharia social) e justificativa curta.
- **IA só acima do limiar heurístico**: remetente já em blocklist responde sem chamar IA (contenção de custo — ADR-0005).
- Cache por **hash de conteúdo** (ADR-0015) evita revalidar mensagens repetidas entre instalações.

### Links

- Fonte principal: **Google Safe Browsing API** (`threatMatches.find`) — determinística e rápida.
- **Normalização/canonicalização** da URL antes do lookup (deduplicação e cache).
- IA analisa **contexto** (ex.: link escondido atrás de texto, domínio similar a legítimo); **nunca acessa o link**.

### Transparência

Persistir `score`, `nível`, **sinais disparados** e **explicação** (JSONB) — ver entidade `classificacao` no modelo de dados.

## Consequências

Positivas:
- Score único e explicável; overrides dão previsibilidade a casos graves.
- Custo de IA contido (IA seletiva + cache por hash de conteúdo).

Negativas:
- Pesos e limiares são iniciais e precisam de calibração com dados reais.
- Dependência de dois serviços externos (OpenRouter e Safe Browsing).

## Alternativas descartadas

- **IA como único sinal**: cara e sem determinismo para blocklist de links.
- **Regras fixas (sem IA)**: não captura phishing contextual/novo.

## Quando rever

Após os primeiros dados reais de uso, para calibrar pesos/limiares e estimar custo por mensagem (ver `planning/0001-estimativas.md`).
