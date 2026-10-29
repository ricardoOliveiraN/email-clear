"""Score de risco (ADR-0007) e reputação de remetente (ADR-0008)."""

import math

SENDER_MAX = 20
CONTENT_MAX = 70
LINK_MAX = 10
DANGEROUS_SENDER_FLOOR = 80
DANGEROUS_LINK_FLOOR = 85
LEGITIMATE_CONTENT_DISCOUNT = 0.5  # remetente legítimo reduz o risco do conteúdo pela metade

MIN_VOTES = 5
WILSON_THRESHOLD = 0.7


def wilson_lower(positive: int, total: int, z: float = 1.28) -> float:
    """Limite inferior do intervalo de Wilson (confiança 80%)."""
    if total <= 0:
        return 0.0
    phat = positive / total
    z2 = z * z
    denom = 1 + z2 / total
    center = phat + z2 / (2 * total)
    margin = z * math.sqrt((phat * (1 - phat) + z2 / (4 * total)) / total)
    return (center - margin) / denom


def sender_status(
    votos_perigosos: int,
    votos_totais: int,
    min_votes: int = MIN_VOTES,
    threshold: float = WILSON_THRESHOLD,
) -> tuple[str, float]:
    """Estado do remetente: 'dangerous', 'legitimate' ou 'unknown' (+ confiança).

    Contradição é impossível por construção: 'dangerous' exige o limite inferior de
    Wilson dos votos perigosos > threshold, e 'legitimate' exige o limite inferior dos
    votos seguros > threshold. Como perigosos + seguros = total, os dois não podem
    ultrapassar um threshold > 0.5 ao mesmo tempo.
    """
    if votos_totais < min_votes:
        return "unknown", 0.0

    votos_seguros = votos_totais - votos_perigosos
    w_danger = wilson_lower(votos_perigosos, votos_totais)
    w_safe = wilson_lower(votos_seguros, votos_totais)

    if w_danger > threshold:
        return "dangerous", w_danger
    if w_safe > threshold:
        return "legitimate", w_safe
    return "unknown", 0.0


def sender_is_dangerous(
    votos_perigosos: int,
    votos_totais: int,
    min_votes: int = MIN_VOTES,
    threshold: float = WILSON_THRESHOLD,
) -> bool:
    return sender_status(votos_perigosos, votos_totais, min_votes, threshold)[0] == "dangerous"


def sender_is_legitimate(
    votos_perigosos: int,
    votos_totais: int,
    min_votes: int = MIN_VOTES,
    threshold: float = WILSON_THRESHOLD,
) -> bool:
    return sender_status(votos_perigosos, votos_totais, min_votes, threshold)[0] == "legitimate"


def level_from_score(score: int) -> str:
    if score >= 70:
        return "dangerous"
    if score >= 40:
        return "suspicious"
    return "safe"


def combine_score(
    content_score: int,
    sender_votos_perigosos: int,
    sender_votos_totais: int,
    link_dangerous: bool,
) -> tuple[int, str]:
    """Combina os sinais em um score 0–100 e devolve o nível."""
    content_score = max(0, min(CONTENT_MAX, content_score))
    status, _ = sender_status(sender_votos_perigosos, sender_votos_totais)

    if status == "dangerous":
        sender_score = SENDER_MAX
    elif status == "legitimate":
        sender_score = 0
        content_score = round(content_score * LEGITIMATE_CONTENT_DISCOUNT)
    else:
        sender_score = (
            round(SENDER_MAX * wilson_lower(sender_votos_perigosos, sender_votos_totais))
            if sender_votos_totais > 0
            else 0
        )

    link_score = LINK_MAX if link_dangerous else 0
    score = min(100, content_score + sender_score + link_score)

    if status == "dangerous":
        score = max(score, DANGEROUS_SENDER_FLOOR)
    if link_dangerous:
        score = max(score, DANGEROUS_LINK_FLOOR)

    return score, level_from_score(score)
