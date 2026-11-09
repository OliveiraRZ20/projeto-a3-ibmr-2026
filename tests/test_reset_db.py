from quantium_bank import create_app
from quantium_bank.models import db


def test_reset_flow_recreates_schema_before_seeding():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SEED_DEMO_DATA": False,
        }
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        assert {"email", "telefone", "data_nascimento"} <= {
            column.name for column in db.metadata.tables["usuario"].columns
        }
