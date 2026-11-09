import argparse

from .cli import admin, reset_db, run, seed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="quantium_bank")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run.register_parser(subparsers)
    seed.register_parser(subparsers)
    reset_db.register_parser(subparsers)
    admin.register_parser(subparsers)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
