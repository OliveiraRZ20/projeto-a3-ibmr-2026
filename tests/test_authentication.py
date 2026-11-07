import pytest

from app.models import db
from app.services import (
    create_user,
    hash_password,
    validate_password,
    verify_password,
)


def test_password_policy_and_hash():
    assert validate_password("Quantium@01")
    assert not validate_password("abc123")
    password_hash = hash_password("Quantium@01")
    assert password_hash != "Quantium@01"
    assert verify_password("Quantium@01", password_hash)


def test_create_user_rejects_duplicate_cpf(app, database):
    with app.app_context():
        create_user("Ana", "21618722069", "Quantium@01")
        db.session.commit()
        with pytest.raises(ValueError, match="CPF já cadastrado"):
            create_user("Outra Ana", "21618722069", "Quantium@02")
