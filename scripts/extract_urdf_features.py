#!/usr/bin/env python3
"""Extract a minimal embodiment summary from a URDF file (stub).

Install optional dependency: pip install yourdfpy
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def _digest_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def extract_stub(urdf_path: Path) -> dict:
    """Placeholder: returns file digest only. Replace with graph + tabular features."""
    return {
        "urdf_path": str(urdf_path),
        "urdf_digest": _digest_file(urdf_path),
        "features_stub": True,
        "message": "TODO: parse URDF (e.g. yourdfpy) and emit mobility_class, dof_counts, ...",
    }


def main() -> int:
    p = argparse.ArgumentParser(description="URDF → embodiment summary (stub)")
    p.add_argument("--urdf", type=Path, required=True, help="Path to robot.urdf")
    p.add_argument("--out", type=Path, help="Write JSON summary to this path")
    args = p.parse_args()

    if not args.urdf.is_file():
        print(f"error: not a file: {args.urdf}", file=sys.stderr)
        return 1

    summary = extract_stub(args.urdf)
    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
