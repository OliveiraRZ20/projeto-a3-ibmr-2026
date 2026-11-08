from decimal import Decimal

import pytest

from app.models import db
from app.services import create_user, transfer_money

def user_details(prefix: str):
    return {
        "email": f"{prefix}@example.com",
        "telefone": "(21) 99876-5401" if prefix == "ana" else "(21) 98765-4302",
        "data_nascimento": "1990-04-12",
    }


ANA_DETAILS = user_details("ana")
BRUNO_DETAILS = user_details("bruno")


def test_transfer_updates_balances_and_records_transaction(app, database):
    with app.app_context():
        origin = create_user("Ana Lima", "21618722069", "Quantium@01", saldo=Decimal("10.00"), email=ANA_DETAILS["email"], telefone=ANA_DETAILS["telefone"], data_nascimento=ANA_DETAILS["data_nascimento"])
        destination = create_user("Bruno Costa", "21718722095", "Quantium@02", email=BRUNO_DETAILS["email"], telefone=BRUNO_DETAILS["telefone"], data_nascimento=BRUNO_DETAILS["data_nascimento"])
        db.session.commit()
        transaction = transfer_money(origin.id, destination.cpf, "3.25")
        db.session.commit()
        assert transaction.valor == Decimal("3.25")
        assert origin.saldo == Decimal("6.75")
        assert destination.saldo == Decimal("3.25")


@pytest.mark.parametrize(
    ("value", "message"),
    [("0", "mínimo"), ("20", "Saldo insuficiente")],
)
def test_transfer_rejects_invalid_values(app, database, value, message):
    with app.app_context():
        origin = create_user("Ana Lima", "21618722069", "Quantium@01", saldo=Decimal("10.00"), email=ANA_DETAILS["email"], telefone=ANA_DETAILS["telefone"], data_nascimento=ANA_DETAILS["data_nascimento"])
        create_user("Bruno Costa", "21718722095", "Quantium@02", email=BRUNO_DETAILS["email"], telefone=BRUNO_DETAILS["telefone"], data_nascimento=BRUNO_DETAILS["data_nascimento"])
        db.session.commit()
        with pytest.raises(ValueError, match=message):
            transfer_money(origin.id, "21718722095", value)


def test_transfer_rejects_self_transfer(app, database):
    with app.app_context():
        origin = create_user("Ana Lima", "21618722069", "Quantium@01", saldo=Decimal("10.00"), email=ANA_DETAILS["email"], telefone=ANA_DETAILS["telefone"], data_nascimento=ANA_DETAILS["data_nascimento"])
        db.session.commit()
        with pytest.raises(ValueError, match="própria"):
            transfer_money(origin.id, origin.cpf, "1.00")
