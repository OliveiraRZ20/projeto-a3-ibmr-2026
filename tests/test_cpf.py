import pytest

from quantium_bank.objects.cpf import CPF


def test_cpf_validates_and_normalizes():
    assert CPF("216.187.220-69").valor == "21618722069"


def test_cpf_rejects_invalid_value():
    with pytest.raises(ValueError):
        CPF("12345678901")
