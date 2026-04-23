#!/usr/bin/env python3
"""Validate a persona label JSON file against schema/persona_label.schema.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("error: install with  pip install jsonschema", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    schema_path = root / "schema" / "persona_label.schema.json"
    p = argparse.ArgumentParser()
    p.add_argument("label_json", type=Path, help="Path to label .json file")
    args = p.parse_args()

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    instance = json.loads(args.label_json.read_text(encoding="utf-8"))
    jsonschema.validate(instance=instance, schema=schema)
    print("ok:", args.label_json)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except jsonschema.ValidationError as e:
        print("validation error:", e.message, file=sys.stderr)
        raise SystemExit(2)
