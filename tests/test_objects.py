from datetime import date, timedelta

import pytest

from quantium_bank.objects.data_nascimento import DataNascimento
from quantium_bank.objects.email import Email
from quantium_bank.objects.telefone import Telefone


def test_email_normalizes_and_validates():
    assert Email("  Ana@Example.COM ").valor == "ana@example.com"


def test_email_rejects_invalid_structure():
    with pytest.raises(ValueError):
        Email("ana@example")
    with pytest.raises(ValueError):
        Email("ana#test@example.com")


def test_phone_normalizes_brazilian_number():
    phone = Telefone("(21) 99876-5401")
    assert phone.valor == "21998765401"
    assert phone.formatado() == "(21) 99876-5401"


def test_phone_rejects_invalid_ddd():
    with pytest.raises(ValueError):
        Telefone("(01) 99876-5401")


def test_phone_rejects_landline():
    with pytest.raises(ValueError):
        Telefone("(21) 2345-6789")


def test_birth_date_requires_adult():
    adult = date.today().replace(year=date.today().year - 18)
    if (date.today().month, date.today().day) < (adult.month, adult.day):
        adult = adult.replace(year=adult.year - 1)
    assert DataNascimento(adult).valor == adult
    with pytest.raises(ValueError):
        DataNascimento(date.today() - timedelta(days=365))
