import argparse

from ..server_service import run_server


def register_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("run", help="Inicia o servidor de desenvolvimento.")
    parser.set_defaults(handler=execute)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")


def execute(args: argparse.Namespace) -> int:
    run_server(host=args.host, port=args.port, debug=args.debug)
    return 0
