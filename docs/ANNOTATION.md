# Annotation protocol (draft v0.1)

## Goal

Given the **same evidence** every model sees (URDF-derived summary + canonical render), produce a **structured persona** that is plausible for human–robot interaction design and **consistent with embodiment** (locomotion class, manipulation affordances, rough scale).

## Tooling (local)

```bash
pip install -e ".[annotate]"
streamlit run tools/annotate_app.py
```

Reads `data/manifest.csv`, **embeds** the Three.js URDF viewer (iframe; run `python scripts/serve_urdf_viewer.py` at repo root with matching host/port), optional matplotlib thumbnail in an expander, full `embodiment.json`, validates against `schema/persona_label.schema.json`, then **download** or **save** to `data/labels/by_annotator/<annotator_id>/<sample_id>.json`.

## Evidence provided to annotators

1. Canonical render(s) of the robot (fixed camera / lighting — defined per release).
2. Machine-readable **embodiment summary** (joint counts, mobility class, gripper / tool frame flags, joint limits when present, bounding-box scale). Annotators should treat this summary as ground truth for what the robot **can** do physically.

## Output

One JSON object per sample, valid against `schema/persona_label.schema.json`.

### OCEAN (1–5)

Use integers or half-steps if your UI allows; stored as numbers in \[1, 5\]. Rate the **intended public-facing persona** of the robot as a social agent, not your personal mood.

### Behavioral scales (0–1)

Each scale is continuous. Anchor phrases are in the schema descriptions; extend with calibration examples in the pilot spreadsheet.

### Optional `persona_brief`

3–6 sentences, present tense, suitable as a system-prompt seed. **Do not** mention sensors, end-effectors, or locomotion modes **not** present in the embodiment summary.

## Invalid / reject labels

- Any numeric field out of range.
- Text or behavior scales that imply **forbidden** capabilities (e.g., “gentle hugging” for a platform with no suitable arms / contact policy stated in rubric).
- **Contradictions** between OCEAN and behavior scales per the published rubric (to be finalized after pilot).

## Pilot procedure

1. Two independent annotators per sample.
2. If OCEAN vectors differ by more than 2 points on any dimension, or behavior differs by >0.35 on any scale, trigger adjudication (short discussion or third annotator).

## Versioning

Bump `schema_version` in the JSON when fields or ranges change.
