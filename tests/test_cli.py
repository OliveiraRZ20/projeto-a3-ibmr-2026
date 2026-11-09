import pytest

from quantium_bank.__main__ import build_parser
from quantium_bank.cli import reset_db, run, seed


def test_cli_registers_expected_commands():
    parser = build_parser()

    assert parser.parse_args(["run"]).handler is run.execute
    assert parser.parse_args(["seed"]).handler is seed.execute
    assert parser.parse_args(["reset-db"]).handler is reset_db.execute


def test_cli_requires_a_command():
    with pytest.raises(SystemExit):
        build_parser().parse_args([])
