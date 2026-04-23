from __future__ import annotations

import json
from pathlib import Path

import jsonschema


def test_example_label_validates() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "schema" / "persona_label.schema.json").read_text(encoding="utf-8"))
    example = json.loads((root / "examples" / "label.example.json").read_text(encoding="utf-8"))
    jsonschema.validate(instance=example, schema=schema)
