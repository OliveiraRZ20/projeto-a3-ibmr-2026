from decimal import Decimal

from app import create_app
from app.models import Usuario, db
from app.services import create_user

DEMO_USERS = [
    ("Ana Lima", "21618722069", "ana@quantium.test", "21998765401", "1990-04-12", "Quantium@01", "100.00"),
    ("Bruno Costa", "21718722095", "bruno@quantium.test", "21987654302", "1988-09-25", "Quantium@02", "250.00"),
    ("Carla Souza", "21818722011", "carla@quantium.test", "21976543203", "1995-01-08", "Quantium@03", "500.00"),
    ("Diego Alves", "21918722048", "diego@quantium.test", "21965432104", "1987-06-17", "Quantium@04", "750.00"),
    ("Eva Martins", "22018722018", "eva@quantium.test", "21954321005", "1992-11-03", "Quantium@05", "1000.00"),
    ("Felipe Rocha", "22118722044", "felipe@quantium.test", "21943210906", "1985-02-21", "Quantium@06", "1500.00"),
    ("Gabriela Melo", "22218722070", "gabriela@quantium.test", "21932109807", "1998-07-14", "Quantium@07", "2000.00"),
    ("Henrique Dias", "22318722005", "henrique@quantium.test", "21921098708", "1991-12-30", "Quantium@08", "2500.00"),
    ("Isabela Reis", "22418722023", "isabela@quantium.test", "21998017609", "1996-03-19", "Quantium@09", "3000.00"),
    ("Joao Nunes", "22518722050", "joao@quantium.test", "21987026500", "1989-10-27", "Quantium@10", "5000.00"),
]


def seed_demo_users() -> int:
    inserted = 0
    for nome, cpf, email, telefone, data_nascimento, senha, saldo in DEMO_USERS:
        if Usuario.query.filter_by(cpf=cpf).first():
            continue
        create_user(
            nome,
            cpf,
            senha,
            Decimal(saldo),
            email=email,
            telefone=telefone,
            data_nascimento=data_nascimento,
            confirmacao_senha=senha,
        )
        inserted += 1
    db.session.commit()
    return inserted


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print(f"{seed_demo_users()} usuários de demonstração criados.")