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
| `tools/` | Streamlit UI (`annotate_app.py`) + static Three.js URDF viewer (`urdf_viewer/index.html`) |
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

## URDF visualization (Three.js, same stack as gkjohnson/urdf-loaders)

Interactive viewer in the browser (loads `robot.urdf` and resolves `meshes/` next to it):

```bash
python scripts/serve_urdf_viewer.py --port 8765 --open
# or without opening a tab:
python scripts/serve_urdf_viewer.py
```

Then open (default SO-101):  
`http://127.0.0.1:8765/tools/urdf_viewer/index.html?urdf=data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9/robot.urdf`

Uses [urdf-loader](https://www.npmjs.com/package/urdf-loader) + Three.js from CDN (see [live examples](https://gkjohnson.github.io/urdf-loaders/javascript/example/bundle/)).  
**Thumbnail PNG** from STLs only (no URDF tree): `scripts/render_meshes_preview.py` / `close_loop_so101.py`.

## Annotation UI (Streamlit)

```bash
pip install -e ".[annotate]"
streamlit run tools/annotate_app.py
```

Pick a row from `data/manifest.csv`; the app **embeds** the Three.js URDF viewer in the left column (iframe to `serve_urdf_viewer.py`). Optional matplotlib thumbnail lives in a collapsed expander. Then fill OCEAN / behavior / optional text — **download JSON** or **save** under `data/labels/by_annotator/<annotator_id>/<sample_id>.json` (validates against `schema/persona_label.schema.json`).

## Citation

TBD. If you use this repository before a formal publication exists, cite the repository URL and commit hash.

## License

Code in this repository: **MIT** (see `LICENSE`).  
Dataset / annotations may use a separate license (e.g. CC BY 4.0); that will be stated in the dataset card and Croissant metadata when the release is published.
