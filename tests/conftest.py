import pytest

from quantium_bank.models import db


@pytest.fixture
def app():
    from quantium_bank import create_app

    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "SEED_DEMO_DATA": False,
        }
    )


@pytest.fixture
def database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app, database):
    return app.test_client()
