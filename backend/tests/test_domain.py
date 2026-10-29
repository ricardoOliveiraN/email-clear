from app.domain.normalize import (
    content_hash,
    extract_domain,
    extract_urls,
    normalize_sender,
    normalize_url,
)
from app.domain.score import (
    combine_score,
    level_from_score,
    sender_is_dangerous,
    sender_is_legitimate,
    sender_status,
    wilson_lower,
)


def test_wilson_penalizes_small_samples() -> None:
    # 1/1 = 100% mas o limite inferior de Wilson fica bem abaixo de 0.7
    assert wilson_lower(1, 1) < 0.7
    assert wilson_lower(10, 10) > 0.7


def test_sender_is_dangerous_requires_min_votes_and_confidence() -> None:
    assert not sender_is_dangerous(1, 1)  # amostra minúscula (< 5 votos)
    assert not sender_is_dangerous(4, 5)  # não unânime o bastante
    assert sender_is_dangerous(5, 5)  # 5 votos unânimes
    assert sender_is_dangerous(9, 10)


def test_sender_status_is_mutually_exclusive() -> None:
    assert sender_status(5, 5)[0] == "dangerous"  # 5/5 perigosos
    assert sender_status(0, 5)[0] == "legitimate"  # 0 perigosos / 5 seguros
    assert sender_status(3, 5)[0] == "unknown"  # misto → indefinido
    assert sender_status(4, 5)[0] == "unknown"  # não unânime o bastante


def test_sender_is_legitimate() -> None:
    assert sender_is_legitimate(0, 5)
    assert sender_is_legitimate(0, 10)
    assert not sender_is_legitimate(10, 10)
    assert not sender_is_legitimate(5, 10)


def test_level_from_score() -> None:
    assert level_from_score(0) == "safe"
    assert level_from_score(39) == "safe"
    assert level_from_score(40) == "suspicious"
    assert level_from_score(69) == "suspicious"
    assert level_from_score(70) == "dangerous"


def test_combine_score_content_only() -> None:
    score, level = combine_score(30, 0, 0, False)
    assert score == 30
    assert level == "safe"


def test_combine_score_high_content_reaches_suspicious() -> None:
    # IA confiante (ex.: 95/100 → conteúdo ~66/70) deve sair de "safe" sozinha
    score, level = combine_score(66, 0, 0, False)
    assert score == 66
    assert level == "suspicious"


def test_combine_score_link_dangerous_floor() -> None:
    score, level = combine_score(0, 0, 0, True)
    assert score >= 85
    assert level == "dangerous"


def test_combine_score_dangerous_sender_floor() -> None:
    score, level = combine_score(0, 10, 10, False)
    assert score >= 80
    assert level == "dangerous"


def test_combine_score_legitimate_sender_discounts_content() -> None:
    # remetente legítimo (0 perigosos / 10 votos) reduz o conteúdo pela metade
    score, level = combine_score(66, 0, 10, False)
    assert score == 33
    assert level == "safe"


def test_normalize_sender() -> None:
    assert normalize_sender("  Alice@Example.COM ") == "alice@example.com"


def test_extract_domain() -> None:
    assert extract_domain("alice@sub.example.com") == "sub.example.com"
    assert extract_domain("example.com") == "example.com"


def test_normalize_url() -> None:
    assert normalize_url("HTTPS://Example.COM:443/Path#frag") == "https://example.com/Path"
    assert normalize_url("http://example.com:80") == "http://example.com/"


def test_extract_urls() -> None:
    text = "veja http://a.example.com/x e https://b.example.com/y"
    urls = extract_urls(text)
    assert "http://a.example.com/x" in urls
    assert "https://b.example.com/y" in urls


def test_content_hash_stable_and_case_insensitive() -> None:
    assert content_hash("A", "B", "C") == content_hash("a", "b", "c")
    assert content_hash("A", "B", "C") != content_hash("A", "B", "D")
