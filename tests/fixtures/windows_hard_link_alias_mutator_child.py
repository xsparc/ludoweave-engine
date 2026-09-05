"""Fixed hard-link alias mutator for the M186 Windows probe."""

from __future__ import annotations

import json
import os
import sys

_SCHEMA = "ludoweave.test.windows-hard-link-alias-mutator/1"
_SOURCE_NAME = r"live\coordination.lock"
_ALIAS_NAME = r"peer\coordination.alias"
_RECREATE_TOKEN = b"+"
_CLOSE_TOKEN = b"!"


def _emit(phase: str) -> None:
    print(
        json.dumps(
            {"phase": phase, "schema": _SCHEMA},
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ),
        flush=True,
    )


def main() -> int:
    if sys.platform != "win32":
        return 2
    if len(sys.argv) != 1:
        return 3

    os.unlink(_ALIAS_NAME)
    _emit("deleted")
    if sys.stdin.buffer.read(1) != _RECREATE_TOKEN:
        return 4

    os.link(_SOURCE_NAME, _ALIAS_NAME)
    _emit("recreated")
    if sys.stdin.buffer.read(1) != _CLOSE_TOKEN:
        return 5

    _emit("closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
