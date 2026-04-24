# embodied-persona-bench

**Embodiment-grounded robot persona specification:** benchmark resources, dataset protocol, and tooling built around versioned URDF snapshots and human-annotated persona labels.

Initial hardware-seeded scope (v0): Unitree A1, TurtleBot3 Burger, XLeRobot, SO-101. URDF-derived graph + tabular features → structured JSON (OCEAN + behavioral scales ± short text).

## Status

Work in progress, targeting **NeurIPS 2026 Evaluations & Datasets** style contribution: **dataset + benchmark + baselines + human-grounded labels**.  
**v0 shipped in-repo:** one full **SO-101 / SO-100** slice (URDF, meshes, `embodiment.json`, preview render, placeholder label, `manifest.csv` row) and scripts to reproduce the pipeline. Other robots (A1, TurtleBot3, XLeRobot) are listed in the schema/manifest but not populated yet.

## For collaborators (what this is)

- **Scientific question:** given a robot’s **embodiment** (URDF / kinematic structure + meshes), specify a **persona** (OCEAN + behavioral control dimensions + short text) that is **consistent with what the body can do** (“physical grounding”), for HRI-style downstream use (prompts, motion style, etc.).
- **What exists today:** JSON schema for labels (`schema/`), annotator draft (`docs/ANNOTATION.md`), URDF→`embodiment.json` extractor (`scripts/extract_urdf_features.py`), one **end-to-end example** (`python scripts/close_loop_so101.py`).
- **Where help is most useful:** (1) **human labels** replacing the SO-101 placeholder + second annotator + adjudication rules, (2) **URDF snapshots** for the other three platforms in the same layout, (3) **baselines + evaluation** code, (4) **hosted dataset** + Croissant metadata before camera-ready.

## Repository layout

| Path | Purpose |
|------|--------|
| `schema/` | JSON Schema for labels and optional manifest records |
| `docs/` | Annotator instructions and rubrics |
| `scripts/` | URDF feature extraction, preview render, loop checks, evaluation (growing) |
| `tools/` | Streamlit annotation UI (`annotate_app.py`) |
| `data/` | Curated v0 assets + manifest; see `data/README.md` (large *future* dumps may live on HF/Dataverse) |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/extract_urdf_features.py --urdf path/to/robot.urdf
# SO-101 / SO-100 (same mechanics) — extract features + write embodiment.json:
python scripts/extract_urdf_features.py \
  --urdf data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9/robot.urdf \
  --robot-family so_101 \
  --out data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9/embodiment.json

# Close the loop (embodiment → sync digest in label → STL preview PNG → schema check):
pip install -e ".[dev]"
python scripts/close_loop_so101.py
```

## Annotation UI (Streamlit)

```bash
pip install -e ".[annotate]"
streamlit run tools/annotate_app.py
```

Opens a browser UI: pick a row from `data/manifest.csv`, see render + `embodiment.json`, fill OCEAN / behavior / optional text, **download JSON** or **save** under `data/labels/by_annotator/<annotator_id>/<sample_id>.json` (validates against `schema/persona_label.schema.json`).

## Citation

TBD. If you use this repository before a formal publication exists, cite the repository URL and commit hash.

## License

Code in this repository: **MIT** (see `LICENSE`).  
Dataset / annotations may use a separate license (e.g. CC BY 4.0); that will be stated in the dataset card and Croissant metadata when the release is published.
