import random
import string
from datetime import date, timedelta
from decimal import Decimal

from faker import Faker

from . import create_app
from .models import Usuario, db
from .services import create_user

DEFAULT_USER_COUNT = 10
MAX_USER_COUNT = 1000
PASSWORD_ALPHABET = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{};:,.?"


def _generate_cpf(rng: random.Random) -> str:
    digits = [rng.randrange(10) for _ in range(9)]
    first = sum(digit * (10 - index) for index, digit in enumerate(digits)) % 11
    digits.append(0 if first < 2 else 11 - first)
    second = sum(digit * (11 - index) for index, digit in enumerate(digits)) % 11
    digits.append(0 if second < 2 else 11 - second)
    return "".join(str(digit) for digit in digits)


def _generate_password(rng: random.Random) -> str:
    required = [rng.choice(string.ascii_uppercase), rng.choice(string.ascii_lowercase)]
    required.extend([rng.choice(string.digits), rng.choice("!@#$%^&*")])
    password = required + [rng.choice(PASSWORD_ALPHABET) for _ in range(8)]
    rng.shuffle(password)
    return "".join(password)


def _generate_phone(rng: random.Random) -> str:
    ddd = rng.choice(
        (11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 24, 27, 28, 31, 32, 33,
         34, 35, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 53, 54, 55,
         61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 73, 74, 75, 77, 79, 81, 82,
         83, 84, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 98, 99)
    )
    number = "9" + str(rng.randrange(10000000, 100000000))
    return f"{ddd}{number}"


def _generate_birth_date(rng: random.Random) -> str:
    oldest = date.today() - timedelta(days=80 * 365)
    youngest = date.today() - timedelta(days=18 * 365 + 1)
    days = rng.randrange((youngest - oldest).days + 1)
    return (oldest + timedelta(days=days)).isoformat()


def _generate_name(fake: Faker) -> str:
    while True:
        name = f"{fake.first_name()} {fake.last_name()}"
        if len(name) <= 100 and all(part.isalpha() for part in name.split()):
            return name


def _validate_count(count: int) -> int:
    if not isinstance(count, int) or count < 0 or count > MAX_USER_COUNT:
        raise ValueError(f"A quantidade deve estar entre 0 e {MAX_USER_COUNT}.")
    return count


def seed_demo_users(
    count: int = DEFAULT_USER_COUNT,
    random_seed: str | int | None = None,
) -> int:
    count = _validate_count(count)
    if Usuario.query.first() is not None:
        return 0
    rng = random.Random(random_seed)
    fake = Faker("pt_BR")
    fake.seed_instance(random_seed)
    existing_cpfs = {user.cpf for user in Usuario.query.all()}
    existing_emails = {user.email for user in Usuario.query.all()}
    existing_phones = {user.telefone for user in Usuario.query.all()}
    generated_credentials: list[tuple[str, str, str]] = []
    inserted = 0
    for index in range(count):
        cpf = _generate_cpf(rng)
        while cpf in existing_cpfs:
            cpf = _generate_cpf(rng)
        nome = _generate_name(fake)
        email = f"usuario{index + 1}.{rng.randrange(100000)}@quantium.test"
        while email in existing_emails:
            email = f"usuario{index + 1}.{rng.randrange(100000)}@quantium.test"
        telefone = _generate_phone(rng)
        while telefone in existing_phones:
            telefone = _generate_phone(rng)
        senha = _generate_password(rng)
        create_user(
            nome,
            cpf,
            senha,
            saldo=Decimal(rng.randrange(0, 500001)) / Decimal("100"),
            email=email,
            telefone=telefone,
            data_nascimento=_generate_birth_date(rng),
            confirmacao_senha=senha,
        )
        existing_cpfs.add(cpf)
        existing_emails.add(email)
        existing_phones.add(telefone)
        generated_credentials.append((nome, cpf, senha))
        inserted += 1
    db.session.commit()
    if generated_credentials:
        print("Credenciais geradas para desenvolvimento:")
        for nome, cpf, senha in generated_credentials:
            print(f"- {nome}: CPF {cpf}, senha {senha}")
    return inserted


def run_seed() -> int:
    app = create_app({"SEED_DEMO_DATA": False})
    with app.app_context():
        count = int(app.config["SEED_USER_COUNT"])
        inserted = seed_demo_users(
            count=count,
            random_seed=app.config["SEED_RANDOM_SEED"],
        )
        print(f"{inserted} usuários criados.")
        return inserted