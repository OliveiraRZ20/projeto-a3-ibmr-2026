import pytest

from quantium_bank.models import db
from quantium_bank.services import (
    create_user,
    hash_password,
    validate_password,
    verify_password,
)

USER_DETAILS = {
    "email": "ana@example.com",
    "telefone": "(21) 99876-5401",
    "data_nascimento": "1990-04-12",
}


def test_password_policy_and_hash():
    assert validate_password("Quantium@01")
    assert not validate_password("abc123")
    assert not validate_password("Quantium @01")
    assert not validate_password("Quantiumá01")
    password_hash = hash_password("Quantium@01")
    assert password_hash != "Quantium@01"
    assert verify_password("Quantium@01", password_hash)


def test_create_user_rejects_duplicate_cpf(app, database):
    with app.app_context():
        create_user(
            "Ana Lima",
            "21618722069",
            "Quantium@01",
            email=USER_DETAILS["email"],
            telefone=USER_DETAILS["telefone"],
            data_nascimento=USER_DETAILS["data_nascimento"],
        )
        db.session.commit()
        with pytest.raises(ValueError, match="CPF já cadastrado"):
            create_user(
                "Outra Ana",
                "21618722069",
                "Quantium@02",
                email="outra@example.com",
                telefone="(21) 98765-4302",
                data_nascimento="1991-04-12",
            )


def test_create_user_validates_profile_data(app, database):
    with app.app_context():
        with pytest.raises(ValueError, match="nome e sobrenome"):
            create_user(
                "Ana",
                "21618722069",
                "Quantium@01",
                email=USER_DETAILS["email"],
                telefone=USER_DETAILS["telefone"],
                data_nascimento=USER_DETAILS["data_nascimento"],
            )
        with pytest.raises(ValueError, match="E-mail inválido"):
            create_user(
                "Ana Lima",
                "21618722069",
                "Quantium@01",
                email="invalid",
                telefone="(21) 99876-5401",
                data_nascimento="1990-04-12",
            )
        with pytest.raises(ValueError, match="somente letras"):
            create_user(
                "Ana 2 Lima",
                "21618722069",
                "Quantium@01",
                email=USER_DETAILS["email"],
                telefone=USER_DETAILS["telefone"],
                data_nascimento=USER_DETAILS["data_nascimento"],
            )
        with pytest.raises(ValueError, match="senhas não coincidem"):
            create_user(
                "Ana Lima",
                "21618722069",
                "Quantium@01",
                confirmacao_senha="Quantium@02",
                email=USER_DETAILS["email"],
                telefone=USER_DETAILS["telefone"],
                data_nascimento=USER_DETAILS["data_nascimento"],
            )


def test_create_user_stores_profile_data_and_timestamps(app, database):
    with app.app_context():
        user = create_user(
            " Ana   Lima ",
            "21618722069",
            "Quantium@01",
            email=USER_DETAILS["email"],
            telefone=USER_DETAILS["telefone"],
            data_nascimento=USER_DETAILS["data_nascimento"],
        )
        db.session.commit()
        assert user.nome == "Ana Lima"
        assert user.email == "ana@example.com"
        assert user.telefone == "21998765401"
        assert user.data_nascimento.isoformat() == "1990-04-12"
        assert user.created_at is not None
        assert user.updated_at is not None


def test_create_user_normalizes_name_title_case(app, database):
    with app.app_context():
        user = create_user(
            " aNA   lIMA ",
            "21618722069",
            "Quantium@01",
            email=USER_DETAILS["email"],
            telefone=USER_DETAILS["telefone"],
            data_nascimento=USER_DETAILS["data_nascimento"],
        )
        assert user.nome == "Ana Lima"
