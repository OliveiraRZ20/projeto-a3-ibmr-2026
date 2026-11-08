import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import event

from .models import db
from .time import format_local_datetime

csrf = CSRFProtect()


def create_app(test_config: dict | None = None) -> Flask:
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            f"sqlite:///{Path(app.instance_path) / 'banco.db'}",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("FLASK_ENV") == "production",
        WTF_CSRF_TIME_LIMIT=None,
        SEED_DEMO_DATA=os.getenv("SEED_DEMO_DATA", "").lower() == "true",
        DISPLAY_TIMEZONE=os.getenv("DISPLAY_TIMEZONE", "America/Sao_Paulo"),
    )
    if test_config:
        app.config.update(test_config)
    app.jinja_env.filters["local_datetime"] = lambda value: format_local_datetime(
        value, app.config["DISPLAY_TIMEZONE"]
    )

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    csrf.init_app(app)

    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        with app.app_context():
            @event.listens_for(db.engine, "connect")
            def enable_sqlite_foreign_keys(connection, _record):
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.close()

    from .routes import register_routes

    register_routes(app)
    with app.app_context():
        db.create_all()
        if app.config["SEED_DEMO_DATA"]:
            from .models import Usuario

            if not Usuario.query.first():
                from seed import seed_demo_users

                seed_demo_users()
    return app