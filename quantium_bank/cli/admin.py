import argparse
import getpass

from .. import create_app
from ..admin_service import create_admin_user, promote_user
from ..models import db


def register_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("admin", help="Gerencia administradores.")
    commands = parser.add_subparsers(dest="admin_command", required=True)

    promote = commands.add_parser(
        "promover",
        help="Promove para administrador um usuário existente.",
    )
    promote.set_defaults(handler=execute_promote)
    promote.add_argument("--cpf", required=True, help="CPF do usuário existente.")

    create = commands.add_parser("criar", help="Cria um novo administrador.")
    create.set_defaults(handler=execute_create)
    create.add_argument("--nome", required=True)
    create.add_argument("--cpf", required=True)
    create.add_argument("--email", required=True)
    create.add_argument("--telefone", required=True)
    create.add_argument("--data-nascimento", required=True)


def execute_promote(args: argparse.Namespace) -> int:
    app = create_app({"SEED_DEMO_DATA": False})
    with app.app_context():
        try:
            user = promote_user(args.cpf)
            print(f"Usuário {user.nome} agora é administrador.")
            return 0
        except (ValueError, OSError) as error:
            db.session.rollback()
            print(f"Erro: {error}")
            return 1


def execute_create(args: argparse.Namespace) -> int:
    senha = getpass.getpass("Senha do administrador: ")
    confirmacao = getpass.getpass("Confirme a senha: ")
    app = create_app({"SEED_DEMO_DATA": False})
    with app.app_context():
        try:
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
