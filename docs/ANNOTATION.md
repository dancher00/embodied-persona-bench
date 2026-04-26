# Annotation protocol (draft v0.1)

## Goal

Given the **same evidence** every annotator sees (URDF-derived summary + 3D model), produce a **structured persona** that is plausible for human–robot interaction design and **consistent with embodiment** (locomotion class, manipulation affordances, rough scale).

## Tooling

### Local (three processes)

```bash
pip install -e ".[annotate,api]"
# Terminal 1 — static files + URDF viewer (default 127.0.0.1:8765)
python scripts/serve_urdf_viewer.py
# Terminal 2 — ratings API (default 127.0.0.1:8000)
export EPB_API_TOKEN="change-me-strong-token"   # optional; if set, Streamlit must use the same token
python -m uvicorn tools.ratings_api:app --host 127.0.0.1 --port 8000
# Terminal 3 — UI
streamlit run tools/annotate_app.py
```

The Streamlit app reads `data/manifest.csv`, **embeds** the Three.js URDF viewer (iframe → `serve_urdf_viewer.py`), shows **`embodiment.json`** in an expander, validates against `schema/persona_label.schema.json`, then either **Submit rating (API)** (`POST /ratings` → SQLite `data/ratings.sqlite3`) or **Download JSON**.

**LAN / multi-seat:** bind viewer and API to `0.0.0.0`, set `EPB_CORS_ORIGINS` to your Streamlit origin (e.g. `http://<host-ip>:8501`), and open Streamlit using the host URL. Details and env vars: repo `README.md`.

### Docker (one container)

See **`README.md` → Docker** and `docker/docker-compose.dev.yml` + `docker/entrypoint.sh` (viewer + API + Streamlit).

## Evidence provided to annotators

1. **Interactive 3D URDF** (meshes as shipped in `data/urdf_snapshots/...`).
2. Machine-readable **embodiment summary** (`embodiment.json`: joint counts, flags, mesh list, `urdf_digest`). Annotators should treat this as ground truth for what the robot **can** do physically.
3. **Canonical render** paths may appear in `manifest.csv` for tooling or thumbnails; the current Streamlit UI does not show manifest PNGs by default.

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
