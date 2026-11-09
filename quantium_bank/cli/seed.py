import argparse

from ..seed_service import run_seed


def register_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("seed", help="Cria usuários fictícios.")
    parser.set_defaults(handler=execute)


def execute(_args: argparse.Namespace) -> int:
    run_seed()
    return 0
