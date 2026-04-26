"""Local Streamlit UI for persona labels (reads data/manifest.csv)."""

from __future__ import annotations

import csv
import json
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

import jsonschema
import streamlit as st
import streamlit.components.v1 as components

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "data" / "manifest.csv"
SCHEMA_PATH = REPO_ROOT / "schema" / "persona_label.schema.json"


@st.cache_data
def load_manifest_rows() -> list[dict[str, str]]:
    if not MANIFEST.is_file():
        return []
    with MANIFEST.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@st.cache_data
def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def main() -> None:
    st.set_page_config(page_title="Embodied persona — annotation", layout="wide")
    st.title("Embodied persona annotation")
    st.caption(
        "Rate the **intended public-facing persona** using the **embedded 3D URDF** and the "
        "**embodiment summary** (expand below). Submit to the ratings API or download JSON. "
        "Do not claim capabilities absent from the embodiment data."
    )

    rows = load_manifest_rows()
    if not rows:
        st.error(f"No rows in {MANIFEST} (relative to {REPO_ROOT}).")
        st.stop()

    sample_ids = [r["sample_id"] for r in rows]
    choice = st.selectbox("Sample", sample_ids, index=0)
    row = next(r for r in rows if r["sample_id"] == choice)

    vport = 8765
    vhost = "127.0.0.1"
    vheight = 900
    urdf_rel = row["urdf_relative"].replace("\\", "/")
    # `v` busts iframe cache after viewer HTML changes; `frame=ros` aligns URDF Z-up with Three.js Y-up grid.
    viewer_q = urllib.parse.urlencode({"urdf": urdf_rel, "frame": "ros", "v": "3"})
    viewer_url = f"http://{vhost}:{int(vport)}/tools/urdf_viewer/index.html?{viewer_q}"
    api_base = "http://127.0.0.1:8000"

    emb_path = REPO_ROOT / row["embodiment_json_relative"]
    if not emb_path.is_file():
        st.error(f"Missing embodiment: {emb_path}")
        st.stop()
    embodiment = json.loads(emb_path.read_text(encoding="utf-8"))
    digest = embodiment.get("urdf_digest", "")

    st.subheader("Robot (URDF + meshes)")
    st.caption(
        "Drag to orbit · scroll to zoom. The iframe loads the same page as "
        "`python scripts/serve_urdf_viewer.py` (here: **127.0.0.1:8765**). "
        "On another machine, open Streamlit via the host LAN IP and run the viewer/API bound to "
        "`0.0.0.0` — see repo `README.md`."
    )
    components.iframe(src=viewer_url, height=int(vheight), scrolling=False)
    st.caption(
        "Blank 3D panel → start the viewer from the repo root, e.g. "
        "`python scripts/serve_urdf_viewer.py --host 127.0.0.1 --port 8765`."
    )
    with st.expander("Embodiment summary (`embodiment.json`)", expanded=False):
        st.json(embodiment)

    st.divider()
    annotator = st.text_input(
        "Annotator id (short, e.g. `alice`)",
        value="",
        key="annotator_id",
    ).strip().lower()
    api_token = st.text_input("API bearer token (optional)", value="", type="password")

    def _annotator_ok(s: str) -> bool:
        if not s or len(s) > 48:
            return False
        return all(c.isalnum() or c in "_-" for c in s)

    if not _annotator_ok(annotator):
        st.info("Set annotator id (1–48 chars: letters, digits, `_`, `-`) to enable **Submit rating (API)**.")

    sid = row["sample_id"]
    st.subheader("OCEAN (1–5)")
    oc1, oc2, oc3, oc4, oc5 = st.columns(5)
    with oc1:
        o = st.slider("Openness", 1.0, 5.0, 3.0, 0.5, key=f"o_{sid}")
    with oc2:
        c = st.slider("Conscientiousness", 1.0, 5.0, 3.0, 0.5, key=f"c_{sid}")
    with oc3:
        e = st.slider("Extraversion", 1.0, 5.0, 3.0, 0.5, key=f"e_{sid}")
    with oc4:
        a = st.slider("Agreeableness", 1.0, 5.0, 3.0, 0.5, key=f"a_{sid}")
    with oc5:
        n = st.slider("Neuroticism", 1.0, 5.0, 3.0, 0.5, key=f"n_{sid}")

    st.subheader("Behavior (0–1)")
    b1, b2 = st.columns(2)
    with b1:
        mt = st.slider("Motion tempo (slow → fast)", 0.0, 1.0, 0.5, 0.05, key=f"mt_{sid}")
        ip = st.slider("Interaction proactivity (reactive → initiating)", 0.0, 1.0, 0.5, 0.05, key=f"ip_{sid}")
    with b2:
        lf = st.slider("Linguistic formality (informal → formal)", 0.0, 1.0, 0.5, 0.05, key=f"lf_{sid}")
        eh = st.slider("Error handling (withdrawn → direct)", 0.0, 1.0, 0.5, 0.05, key=f"eh_{sid}")

    brief = st.text_area(
        "Persona brief (optional, 3–6 sentences)",
        height=160,
        placeholder="Present tense. No sensors/grippers/locomotion not in the embodiment summary.",
        key=f"brief_{sid}",
    )
    notes = st.text_area("Internal notes (optional)", height=80, key=f"notes_{sid}")

    label: dict = {
        "schema_version": "0.1.0",
        "sample_id": row["sample_id"],
        "robot_family": row["robot_family"],
        "urdf_digest": digest,
        "ocean": {
            "openness": float(o),
            "conscientiousness": float(c),
            "extraversion": float(e),
            "agreeableness": float(a),
            "neuroticism": float(n),
        },
        "behavior": {
            "motion_tempo": float(mt),
            "interaction_proactivity": float(ip),
            "linguistic_formality": float(lf),
            "error_handling_style": float(eh),
        },
    }
    if brief.strip():
        label["persona_brief"] = brief.strip()
    if notes.strip():
        label["notes_internal"] = notes.strip()

    err = None
    try:
        jsonschema.validate(instance=label, schema=load_schema())
    except jsonschema.ValidationError as ve:
        err = str(ve.message)

    dl = st.download_button(
        "Download JSON",
        data=json.dumps(label, indent=2, sort_keys=True) + "\n",
        file_name=f"{row['sample_id']}.{annotator or 'anon'}.json",
        mime="application/json",
        disabled=bool(err),
    )
    if dl:
        st.success("Download started.")

    if st.button("Submit rating (API)", disabled=not _annotator_ok(annotator) or bool(err)):
        if err:
            st.error(err)
        else:
            body = json.dumps({"annotator_id": annotator, "label": label}).encode("utf-8")
            req = urllib.request.Request(
                url=f"{api_base}/ratings",
                data=body,
                headers={
                    "Content-Type": "application/json",
                    **({"Authorization": f"Bearer {api_token}"} if api_token else {}),
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    response_data = json.loads(resp.read().decode("utf-8"))
                st.success(
                    f"Saved rating id={response_data.get('id')} at {response_data.get('created_at')} (UTC)."
                )
            except urllib.error.HTTPError as http_err:
                details = http_err.read().decode("utf-8", errors="replace")
                st.error(f"API error {http_err.code}: {details}")
            except urllib.error.URLError as url_err:
                st.error(f"Failed to reach API at {api_base}: {url_err.reason}")


if __name__ == "__main__":
    main()
