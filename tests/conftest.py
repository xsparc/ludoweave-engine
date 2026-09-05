"""Make repository-only test helpers available to both pytest entry points."""

from __future__ import annotations

import sys
from pathlib import Path

# The console script does not add cwd as `python -m pytest` does. This path
# contains test helpers, not an alternative installed ludoweave package.
_REPOSITORY_ROOT = str(Path(__file__).resolve().parents[1])
if _REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, _REPOSITORY_ROOT)
