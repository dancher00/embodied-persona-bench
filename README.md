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
conda create -n embodied-persona-bench python=3.10 -y
conda activate embodied-persona-bench
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
pip install -e ".[annotate,api]"
export EPB_API_TOKEN="change-me-strong-token"
export EPB_CORS_ORIGINS="http://127.0.0.1:8501,http://localhost:8501"
python -m uvicorn tools.ratings_api:app --host 127.0.0.1 --port 8000
streamlit run tools/annotate_app.py
```

Pick a row from `data/manifest.csv`; the app **embeds** the Three.js URDF viewer (iframe → `serve_urdf_viewer.py` on **127.0.0.1:8765**) and shows **`embodiment.json`** in an expander. Fill OCEAN / behavior / optional text — **download JSON** or **submit rating (API)** to SQLite at **127.0.0.1:8000** (validates against `schema/persona_label.schema.json`). Optional manifest thumbnails are for other tooling; use `scripts/render_meshes_preview.py` where STLs exist.

Ratings API helpers:
- `GET /health` — liveness check
- `GET /ratings?limit=100` — recent ratings JSON
- `GET /ratings.csv` — CSV export
- `POST /ratings` — create/update by unique pair `(annotator_id, sample_id)`

Security env vars for API:
- `EPB_API_TOKEN` — required bearer token for `POST /ratings` (if unset, auth is disabled for local dev)
- `EPB_CORS_ORIGINS` — comma-separated allowed origins
- `EPB_RATE_LIMIT_PER_MIN` — requests/minute/IP for `POST /ratings` (default `60`)
- `EPB_MAX_BODY_BYTES` — max request size in bytes (default `131072`)

## Run in local network (LAN)

If you want other devices in the same network to open the app and submit ratings, run all services bound to `0.0.0.0` on the host machine.

Host machine (from repo root, in `conda` env):

```bash
# Terminal 1: URDF static viewer (Three.js assets)
python scripts/serve_urdf_viewer.py --host 0.0.0.0 --port 8765

# Terminal 2: Ratings API (SQLite)
export EPB_API_TOKEN="change-me-strong-token"
export EPB_CORS_ORIGINS="http://<HOST_IP>:8501"
python -m uvicorn tools.ratings_api:app --host 0.0.0.0 --port 8000

# Terminal 3: Streamlit UI
streamlit run tools/annotate_app.py --server.address 0.0.0.0 --server.port 8501
```

Then share this URL with clients in the same LAN:

- `http://<HOST_IP>:8501`

Where `<HOST_IP>` is the host machine local IP (example: `192.168.31.153`).

The Streamlit app currently hardcodes **127.0.0.1** for the viewer iframe and API URL, so the browser that runs the UI should be on the **same machine** as `serve_urdf_viewer.py`, `uvicorn`, and Streamlit (typical lab setup), or use **Docker** on the host so all three services share one origin stack. Remote laptops opening only `http://<HOST_IP>:8501` would still try to load the viewer from the laptop’s own loopback — that path needs a future configurable host if you want cross-machine browsers.

**API bearer token** in the UI: same value as `EPB_API_TOKEN` when the API enforces auth.

Quick checks from a client device:

- `http://<HOST_IP>:8765/tools/urdf_viewer/index.html` (viewer responds)
- `http://<HOST_IP>:8000/health` (API responds)
- `http://<HOST_IP>:8501` (annotation UI opens)

## Docker (single container, 3 services)

For active development, use bind mount (no rebuild needed after code edits):

```bash
cd docker
export EPB_API_TOKEN="change-me-strong-token"
export EPB_CORS_ORIGINS="http://<HOST_IP>:8501"
docker compose -f docker-compose.dev.yml up
```

This mode mounts the repo into the container (`..:/app`), so app changes apply on restart without rebuilding an image.

If you need an immutable image for deployment, use the Dockerfile flow:

```bash
cd docker
docker build -f Dockerfile -t embodied-persona-bench:local ..
docker run --rm -it \
  -p 8501:8501 -p 8000:8000 -p 8765:8765 \
  -e EPB_API_TOKEN="change-me-strong-token" \
  -e EPB_CORS_ORIGINS="http://<HOST_IP>:8501" \
  embodied-persona-bench:local
```

Container starts:
- Streamlit: `8501`
- Ratings API: `8000`
- URDF viewer static server: `8765`

Optional overrides:
- `HOST_ADDR` (default `0.0.0.0`)
- `VIEWER_PORT` (default `8765`)
- `API_PORT` (default `8000`)
- `STREAMLIT_PORT` (default `8501`)

## Citation

TBD. If you use this repository before a formal publication exists, cite the repository URL and commit hash.

## License

Code in this repository: **MIT** (see `LICENSE`).  
Dataset / annotations may use a separate license (e.g. CC BY 4.0); that will be stated in the dataset card and Croissant metadata when the release is published.
