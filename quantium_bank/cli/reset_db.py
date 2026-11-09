import argparse

from ..database_service import reset_database


def register_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("reset-db", help="Recria o banco de desenvolvimento.")
    parser.set_defaults(handler=execute)


def execute(_args: argparse.Namespace) -> int:
    reset_database()
    return 0
