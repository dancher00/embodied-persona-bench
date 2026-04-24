from __future__ import annotations

import json
from pathlib import Path

import jsonschema


def test_so101_placeholder_label_validates() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = json.loads((root / "schema/persona_label.schema.json").read_text(encoding="utf-8"))
    label_path = root / "data/labels/so101_brukg_5e97ca9.placeholder.json"
    instance = json.loads(label_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=instance, schema=schema)
