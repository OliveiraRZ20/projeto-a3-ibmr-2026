import sys

import pytest

import admin
from admin import create_admin_user, promote_user
from app.models import Usuario, db
from app.services import create_user


def test_promote_user_marks_existing_user_as_admin(app, database):
    with app.app_context():
        create_user(
            "Ana Lima",
            "21618722069",
            "Quantium@01",
            email="ana@example.com",
            telefone="(21) 99876-5401",
            data_nascimento="1990-04-12",
        )
        db.session.commit()

        user = promote_user("216.187.220-69")

        assert user.is_admin is True
        assert Usuario.query.filter_by(is_admin=True).count() == 1


def test_promote_user_rejects_unknown_cpf(app, database):
    with app.app_context():
        with pytest.raises(ValueError, match="Usuário não encontrado"):
            promote_user("21718722095")


def test_create_admin_user_uses_domain_validation(app, database):
    with app.app_context():
        user = create_admin_user(
            nome="Ana Lima",
            cpf="21618722069",
            email="ana@example.com",
            telefone="(21) 99876-5401",
            data_nascimento="1990-04-12",
            senha="Quantium@01",
            confirmacao_senha="Quantium@01",
        )

        assert user.is_admin is True
        assert user.senha != "Quantium@01"


def test_main_handles_unknown_cpf_without_losing_application_context(
    app, monkeypatch, capsys
):
    monkeypatch.setattr(admin, "create_app", lambda _config: app)
    monkeypatch.setattr(
        sys,
        "argv",
        ["admin.py", "promover", "--cpf", "21718722095"],
    )

    assert admin.main() == 1
    assert "Erro: Usuário não encontrado" in capsys.readouterr().out
