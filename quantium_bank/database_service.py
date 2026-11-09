from . import create_app
from .models import db
from .seed_service import seed_demo_users


def reset_database() -> int:
    app = create_app({"SEED_DEMO_DATA": False})
    with app.app_context():
        db.drop_all()
        db.create_all()
        inserted = seed_demo_users(
            count=app.config["SEED_USER_COUNT"],
            random_seed=app.config["SEED_RANDOM_SEED"],
        )
        print(f"{inserted} usuários criados após o reset.")
        return inserted