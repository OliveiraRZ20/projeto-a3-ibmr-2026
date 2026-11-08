from decimal import Decimal

from app.models import db
from app.services import create_user, transfer_money


def _create_user(name, cpf, email, phone, is_admin=False, saldo="0.00"):
    return create_user(
        name,
        cpf,
        "Quantium@01",
        email=email,
        telefone=phone,
        data_nascimento="1990-04-12",
        saldo=Decimal(saldo),
        is_admin=is_admin,
    )


def test_admin_panel_requires_admin_user(client):
    response = client.get("/admin")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_regular_user_cannot_access_admin_panel(app, database):
    with app.app_context():
        user = _create_user(
            "Ana Lima",
            "21618722069",
            "ana@example.com",
            "(21) 99876-5401",
        )
        user_cpf = user.cpf
        db.session.commit()

    client = app.test_client()
    client.post("/login", data={"cpf": user_cpf, "senha": "Quantium@01"})
    response = client.get("/admin")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/dashboard")


def test_admin_can_view_metrics_and_filtered_data(app, database):
    with app.app_context():
        admin = _create_user(
            "Ana Lima",
            "21618722069",
            "ana@example.com",
            "(21) 99876-5401",
            is_admin=True,
            saldo="10.00",
        )
        admin_cpf = admin.cpf
        destination = _create_user(
            "Bruno Costa",
            "21718722095",
            "bruno@example.com",
            "(21) 98765-4302",
        )
        db.session.commit()
        transfer_money(admin.id, destination.cpf, "3.25")
        db.session.commit()

    client = app.test_client()
    client.post("/login", data={"cpf": admin_cpf, "senha": "Quantium@01"})

    dashboard = client.get("/admin")
    users = client.get("/admin/usuarios?q=Bruno")
    transactions = client.get("/admin/transacoes?cpf=21618722069&minimo=3")

    assert dashboard.status_code == 200
    assert b"R$ 10,00" in dashboard.data
    assert b"R$ 3,25" in dashboard.data
    assert users.status_code == 200
    assert b"Bruno Costa" in users.data
    assert transactions.status_code == 200
    assert b"Bruno Costa" in transactions.data
