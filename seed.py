from decimal import Decimal

from app import create_app
from app.models import Usuario, db
from app.services import create_user

DEMO_USERS = [
    ("Ana Lima", "21618722069", "Quantium@01", "100.00"),
    ("Bruno Costa", "21718722095", "Quantium@02", "250.00"),
    ("Carla Souza", "21818722011", "Quantium@03", "500.00"),
    ("Diego Alves", "21918722048", "Quantium@04", "750.00"),
    ("Eva Martins", "22018722018", "Quantium@05", "1000.00"),
    ("Felipe Rocha", "22118722044", "Quantium@06", "1500.00"),
    ("Gabriela Melo", "22218722070", "Quantium@07", "2000.00"),
    ("Henrique Dias", "22318722005", "Quantium@08", "2500.00"),
    ("Isabela Reis", "22418722023", "Quantium@09", "3000.00"),
    ("Joao Nunes", "22518722050", "Quantium@10", "5000.00"),
]


def seed_demo_users() -> int:
    inserted = 0
    for nome, cpf, senha, saldo in DEMO_USERS:
        if Usuario.query.filter_by(cpf=cpf).first():
            continue
        create_user(nome, cpf, senha, Decimal(saldo))
        inserted += 1
    db.session.commit()
    return inserted


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print(f"{seed_demo_users()} usuários de demonstração criados.")