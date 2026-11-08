import re
from decimal import Decimal, InvalidOperation

import bcrypt
from sqlalchemy import text

from .models import Transacao, Usuario, db
from .objects.cpf import CPF
from .objects.data_nascimento import DataNascimento
from .objects.email import Email
from .objects.telefone import Telefone

PASSWORD_PATTERN = re.compile(
    r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};:,.?])"
    r"[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:,.?]{6,}$"
)


def validate_password(password: str) -> bool:
    return bool(PASSWORD_PATTERN.fullmatch(password or ""))


def hash_password(password: str) -> str:
    if not validate_password(password):
        raise ValueError(
            "A senha deve ter pelo menos 6 caracteres, usando letras, números "
            "e caracteres especiais permitidos."
        )
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def normalize_cpf(value: str) -> str:
    return CPF(value).valor


def _normalize_name(value: str) -> str:
    normalized = " ".join(value.split()) if isinstance(value, str) else ""
    parts = normalized.split()
    if len(parts) < 2:
        raise ValueError("Informe nome e sobrenome.")
    if not all(part.isalpha() for part in parts):
        raise ValueError("O nome deve conter somente letras e espaços.")
    if len(normalized) > 100:
        raise ValueError("O nome completo deve ter no máximo 100 caracteres.")
    return normalized.title()


def create_user(
    nome: str,
    cpf: str,
    senha: str,
    saldo: Decimal = Decimal("0.00"),
    email: str | None = None,
    telefone: str | None = None,
    data_nascimento: str | None = None,
    confirmacao_senha: str | None = None,
):
    normalized = normalize_cpf(cpf)
    normalized_name = _normalize_name(nome)
    normalized_email = Email(email or "").valor
    normalized_phone = Telefone(telefone or "").valor
    birth_date = DataNascimento(data_nascimento or "").valor
    if Usuario.query.filter_by(cpf=normalized).first():
        raise ValueError("CPF já cadastrado.")
    if Usuario.query.filter_by(email=normalized_email).first():
        raise ValueError("E-mail já cadastrado.")
    if confirmacao_senha is not None and senha != confirmacao_senha:
        raise ValueError("As senhas não coincidem.")
    user = Usuario(
        nome=normalized_name,
        cpf=normalized,
        email=normalized_email,
        telefone=normalized_phone,
        data_nascimento=birth_date,
        senha=hash_password(senha),
        saldo=saldo,
    )
    db.session.add(user)
    return user


def transfer_money(origin_id: int, destination_cpf: str, raw_value: str) -> Transacao:
    try:
        value = Decimal(raw_value).quantize(Decimal("0.01"))
    except (InvalidOperation, TypeError):
        raise ValueError("Valor de transferência inválido.")
    if value < Decimal("0.01"):
        raise ValueError("O valor mínimo é R$ 0,01.")

    db.session.execute(text("BEGIN IMMEDIATE"))
    origin = db.session.get(Usuario, origin_id)
    destination = Usuario.query.filter_by(cpf=normalize_cpf(destination_cpf)).first()
    if origin is None:
        raise ValueError("Conta de origem não encontrada.")
    if destination is None:
        raise ValueError("CPF de destino não encontrado.")
    if origin.id == destination.id:
        raise ValueError("Não é possível transferir para a própria conta.")
    if Decimal(origin.saldo) < value:
        raise ValueError("Saldo insuficiente.")

    origin.saldo = Decimal(origin.saldo) - value
    destination.saldo = Decimal(destination.saldo) + value
    transaction = Transacao(
        conta_origem_id=origin.id,
        conta_destino_id=destination.id,
        valor=value,
    )
    db.session.add(transaction)
    return transaction
