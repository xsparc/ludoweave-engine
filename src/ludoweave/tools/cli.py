"""Standard-library command-line interface for the M0 engine skeleton."""

import argparse
import json
from collections.abc import Sequence

from ludoweave import __version__
from ludoweave.tools.doctor import run_doctor


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ludoweave",
        description="Deterministic, headless-first Python engine for agent-operable 2D worlds.",
    )
    parser.add_argument("--version", action="version", version=f"ludoweave {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("doctor", help="run structured local environment diagnostics")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""

    parser = _build_parser()
    args = parser.parse_args(argv)
    command: object = getattr(args, "command", None)
    if command == "doctor":
        report, exit_code = run_doctor()
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))
        return exit_code
    parser.print_help()
    return 0
