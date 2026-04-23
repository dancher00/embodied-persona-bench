# embodied-persona-bench

**Embodiment-grounded robot persona specification:** benchmark resources, dataset protocol, and tooling built around versioned URDF snapshots and human-annotated persona labels.

Initial hardware-seeded scope (v0): Unitree A1, TurtleBot3 Burger, XLeRobot, SO-101. URDF-derived graph + tabular features → structured JSON (OCEAN + behavioral scales ± short text).

## Status

Work in progress. Schema and annotation docs are versioned here; full release will include hosted dataset (Croissant metadata per venue guidelines) and evaluation scripts.

## Repository layout

| Path | Purpose |
|------|--------|
| `schema/` | JSON Schema for labels and optional manifest records |
| `docs/` | Annotator instructions and rubrics |
| `scripts/` | URDF feature extraction, split utilities, evaluation |
| `data/` | **Not** checked in: large URDFs, meshes, renders; see `data/README.md` |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python scripts/extract_urdf_features.py --urdf path/to/robot.urdf
```

## Citation

TBD. If you use this repository before a formal publication exists, cite the repository URL and commit hash.

## License

Code in this repository: **MIT** (see `LICENSE`).  
Dataset / annotations may use a separate license (e.g. CC BY 4.0); that will be stated in the dataset card and Croissant metadata when the release is published.
