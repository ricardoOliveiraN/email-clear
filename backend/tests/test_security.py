from app.core.security import (
    hash_install_id,
    new_install_id,
    sign_install_id,
    verify_install_token,
)

SECRET = "s3cret-token"


def test_token_roundtrip() -> None:
    install_id = new_install_id()
    token = sign_install_id(install_id, SECRET)
    assert verify_install_token(token, SECRET) == install_id


def test_token_rejects_tampering() -> None:
    install_id = new_install_id()
    token = sign_install_id(install_id, SECRET)
    assert verify_install_token("x" + token, SECRET) is None


def test_token_rejects_wrong_secret() -> None:
    install_id = new_install_id()
    token = sign_install_id(install_id, SECRET)
    assert verify_install_token(token, "outro-segredo") is None


def test_token_rejects_malformed() -> None:
    assert verify_install_token("sem-ponto", SECRET) is None


def test_hash_stable_and_distinct() -> None:
    assert hash_install_id("abc") == hash_install_id("abc")
    assert hash_install_id("abc") != hash_install_id("abd")
