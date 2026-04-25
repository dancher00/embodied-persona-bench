# Data directory

**Small curated snapshots** (URDF + meshes + JSON + preview PNG) live in git for v0. Very large corpora or raw logs should go to **Hugging Face / Dataverse** (see NeurIPS ED hosting guidelines).

Layout:

```text
data/
  urdf_snapshots/     # see urdf_snapshots/NAMING.md — where to copy official URDFs
  renders/            # PNGs shown to annotators
  labels/             # JSON lines, one label per file or consolidated with split column
  manifest.csv        # v0: manifest rows per snapshot (URDF + embodiment + render + split)
```

**URDF drop-in guide:** `data/urdf_snapshots/NAMING.md`  
**SO-101 / SO-100 closed loop:** `brukg_SO-100-arm_5e97ca9/` (`robot.urdf`, `meshes/`, `embodiment.json`) + optional `data/renders/so101_brukg_5e97ca9/preview.png` (matplotlib STL thumbnail) + `data/labels/so101_brukg_5e97ca9.placeholder.json`. Run `python scripts/close_loop_so101.py` after `.[dev]` install to regenerate the thumbnail and JSON. For **assembled URDF in the browser**, run `python scripts/serve_urdf_viewer.py` and open the URL from the repo `README.md`. Manifest: `data/manifest.csv` (see also `manifest.example.csv`).

**Unitree A1 (v0 snapshot):** `unitree_a1/a1_ros1_pkg_2026-04-25/` — `robot.urdf` (mesh paths `meshes/*.dae`), `embodiment.json`, `PROVENANCE.txt`. Meshes are Collada; use the URDF viewer in Streamlit or `serve_urdf_viewer.py`. Manifest row `a1_ros1_pkg_2026-04-25` reserves a matplotlib PNG path; thumbnail can be added later (DAE-only folder).

**NAO (v0 snapshot):** `nao/jrl_v40_6f4e94b/` — NAO V40 humanoid from [jrl-umi3218/nao_description](https://github.com/jrl-umi3218/nao_description) @ `6f4e94b` (BSD-2-Clause). Includes `meshes/V40/*.dae` and shared `meshes/V40/textureNAO.png` for Collada textures. Many ROS `nao_description` trees omit meshes (separate install); this fork carries them in-repo.

For NeurIPS Evaluations & Datasets track, the public release will be hosted on a designated platform (e.g. Hugging Face) with **Croissant** metadata (core + Responsible AI fields).

## Robot families (v0)

| `robot_family`   | Notes |
|------------------|--------|
| `unitree_a1`     | Quadruped snapshot you pin in the manifest |
| `turtlebot3_burger` | Differential drive |
| `xlerobot`       | Pin exact hardware revision / URDF package version |
| `so_101`         | SO-100/SO-101 arm (flat URDF + meshes); see `brukg_SO-100-arm_5e97ca9/` |
| `nao`            | SoftBank / Aldebaran NAO; see `nao/jrl_v40_6f4e94b/` |

Record provenance (upstream repo URL + commit or ROS package version) in `manifest.csv` or dataset card.

**Human labels:** use the Streamlit app (`streamlit run tools/annotate_app.py`, see repo `README.md`) or any editor; store under `data/labels/by_annotator/<id>/` for multi-annotator agreement.
