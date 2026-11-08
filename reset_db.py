from app import create_app
from app.models import db
from seed import seed_demo_users


if __name__ == "__main__":
    app = create_app({"SEED_DEMO_DATA": False})
    with app.app_context():
        db.drop_all()
        db.create_all()
        print(f"{seed_demo_users()} usuários criados após o reset.")