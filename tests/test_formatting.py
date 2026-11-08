from decimal import Decimal


def test_cpf_filter_formats_normalized_value(app):
    with app.app_context():
        cpf_filter = app.jinja_env.filters["cpf"]
        assert cpf_filter("21618722069") == "216.187.220-69"
        assert cpf_filter("invalid") == "invalid"


def test_money_filter_formats_brazilian_currency(app):
    with app.app_context():
        money_filter = app.jinja_env.filters["money"]
        assert money_filter(Decimal("19101.08")) == "R$ 19.101,08"
