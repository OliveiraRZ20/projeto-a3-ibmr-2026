from datetime import datetime, timezone

from app.models import db
from app.services import create_user


def test_profile_requires_authentication(client):
    response = client.get("/perfil")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_local_datetime_filter_converts_utc_to_display_timezone(app):
    value = datetime(2026, 1, 15, 15, 30, tzinfo=timezone.utc)
    with app.app_context():
        assert app.jinja_env.filters["local_datetime"](value) == "15/01/2026 12:30"


def test_orphaned_session_is_cleared(client):
    with client.session_transaction() as session:
        session["user_id"] = 9999

    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
    with client.session_transaction() as session:
        assert "user_id" not in session


def test_authenticated_user_can_view_read_only_profile(app, database):
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

    client = app.test_client()
    login_response = client.post(
        "/login",
        data={"cpf": "21618722069", "senha": "Quantium@01"},
    )
    assert login_response.status_code == 302

    response = client.get("/perfil")
    assert response.status_code == 200
    assert b"ana@example.com" in response.data
    assert b"21) 99876-5401" in response.data
    assert b'name="email"' not in response.data
