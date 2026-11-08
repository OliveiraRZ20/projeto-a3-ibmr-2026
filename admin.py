import argparse
import getpass

from app import create_app
from app.models import Usuario, db
from app.services import create_user, normalize_cpf


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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Gerencia usuários administradores do Quantium Bank."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    promote = subparsers.add_parser(
        "promover",
        help="Promove para administrador um usuário existente.",
    )
    promote.add_argument("--cpf", required=True, help="CPF do usuário existente.")

    create = subparsers.add_parser(
        "criar",
        help="Cria um novo usuário administrador.",
    )
    create.add_argument("--nome", required=True)
    create.add_argument("--cpf", required=True)
    create.add_argument("--email", required=True)
    create.add_argument("--telefone", required=True)
    create.add_argument("--data-nascimento", required=True)

    return parser


def main() -> int:
    args = _build_parser().parse_args()
    app = create_app({"SEED_DEMO_DATA": False})

    try:
        with app.app_context():
            if args.command == "promover":
                user = promote_user(args.cpf)
                print(f"Usuário {user.nome} agora é administrador.")
                return 0

            senha = getpass.getpass("Senha do administrador: ")
            confirmacao = getpass.getpass("Confirme a senha: ")
            user = create_admin_user(
                nome=args.nome,
                cpf=args.cpf,
                email=args.email,
                telefone=args.telefone,
                data_nascimento=args.data_nascimento,
                senha=senha,
                confirmacao_senha=confirmacao,
            )
            print(f"Administrador {user.nome} criado com sucesso.")
            return 0
    except (ValueError, OSError) as error:
        db.session.rollback()
        print(f"Erro: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
