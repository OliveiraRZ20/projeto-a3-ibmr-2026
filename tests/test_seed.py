import pytest

from app.models import Usuario, db
from seed import seed_demo_users


def test_dynamic_seed_creates_unique_valid_users(app, database):
    with app.app_context():
        assert seed_demo_users(count=5, random_seed="test-seed") == 5
        users = Usuario.query.order_by(Usuario.id).all()

        assert len(users) == 5
        assert len({user.cpf for user in users}) == 5
        assert len({user.email for user in users}) == 5
        assert len({user.telefone for user in users}) == 5
        assert sum(user.is_admin for user in users) == 0
        assert all(
            len(user.nome.split()) >= 2
            and all(part.isalpha() for part in user.nome.split())
            for user in users
        )
        assert all(len(user.senha) == 60 for user in users)


def test_dynamic_seed_is_idempotent_with_existing_users(app, database):
    with app.app_context():
        assert seed_demo_users(count=3, random_seed="test-seed") == 3
        assert seed_demo_users(count=3, random_seed="test-seed") == 0
        assert Usuario.query.count() == 3


def test_dynamic_seed_rejects_invalid_count(app, database):
    with app.app_context():
        with pytest.raises(ValueError, match="entre 0 e"):
            seed_demo_users(count=-1)
