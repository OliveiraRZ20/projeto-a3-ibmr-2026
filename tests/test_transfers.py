from decimal import Decimal

import pytest

from app.models import db
from app.services import create_user, transfer_money


def test_transfer_updates_balances_and_records_transaction(app, database):
    with app.app_context():
        origin = create_user("Ana", "21618722069", "Quantium@01", Decimal("10.00"))
        destination = create_user("Bruno", "21718722095", "Quantium@02")
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
        origin = create_user("Ana", "21618722069", "Quantium@01", Decimal("10.00"))
        create_user("Bruno", "21718722095", "Quantium@02")
        db.session.commit()
        with pytest.raises(ValueError, match=message):
            transfer_money(origin.id, "21718722095", value)


def test_transfer_rejects_self_transfer(app, database):
    with app.app_context():
        origin = create_user("Ana", "21618722069", "Quantium@01", Decimal("10.00"))
        db.session.commit()
        with pytest.raises(ValueError, match="própria"):
            transfer_money(origin.id, origin.cpf, "1.00")
