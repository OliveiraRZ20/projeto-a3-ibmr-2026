from .models import Usuario, db
from .services import create_user, normalize_cpf


def promote_user(cpf: str) -> Usuario:
    normalized_cpf = normalize_cpf(cpf)
    user = Usuario.query.filter_by(cpf=normalized_cpf).first()
    if user is None:
        raise ValueError("Usuário não encontrado para o CPF informado.")
    if user.is_admin:
        return user
    user.is_admin = True
    db.session.commit()
    return user


def create_admin_user(
    *,
    nome: str,
    cpf: str,
    email: str,
    telefone: str,
    data_nascimento: str,
    senha: str,
    confirmacao_senha: str,
) -> Usuario:
    user = create_user(
        nome,
        cpf,
        senha,
        email=email,
        telefone=telefone,
        data_nascimento=data_nascimento,
        confirmacao_senha=confirmacao_senha,
        is_admin=True,
    )
    db.session.commit()
    return user

