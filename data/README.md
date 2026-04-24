# Data directory

**Small curated snapshots** (URDF + meshes + JSON + preview PNG) live in git for v0. Very large corpora or raw logs should go to **Hugging Face / Dataverse** (see NeurIPS ED hosting guidelines).

Layout:

```text
data/
  urdf_snapshots/     # see urdf_snapshots/NAMING.md — where to copy official URDFs
  renders/            # PNGs shown to annotators
  labels/             # JSON lines, one label per file or consolidated with split column
  manifest.csv        # v0: one SO-101 row (URDF + embodiment + render + split); extend for other robots
```

**URDF drop-in guide:** `data/urdf_snapshots/NAMING.md`  
**SO-101 / SO-100 closed loop:** `brukg_SO-100-arm_5e97ca9/` (`robot.urdf`, `meshes/`, `embodiment.json`) + `data/renders/so101_brukg_5e97ca9/preview.png` + `data/labels/so101_brukg_5e97ca9.placeholder.json`. Run `python scripts/close_loop_so101.py` after `.[dev]` install to regenerate. Manifest: `data/manifest.csv` (see also `manifest.example.csv`).

For NeurIPS Evaluations & Datasets track, the public release will be hosted on a designated platform (e.g. Hugging Face) with **Croissant** metadata (core + Responsible AI fields).

## Robot families (v0)

| `robot_family`   | Notes |
|------------------|--------|
| `unitree_a1`     | Quadruped snapshot you pin in the manifest |
| `turtlebot3_burger` | Differential drive |
| `xlerobot`       | Pin exact hardware revision / URDF package version |
| `so_101`         | SO-100/SO-101 arm (flat URDF + meshes); see `brukg_SO-100-arm_5e97ca9/` |

Record provenance (upstream repo URL + commit or ROS package version) in `manifest.csv` or dataset card.

**Human labels:** use the Streamlit app (`streamlit run tools/annotate_app.py`, see repo `README.md`) or any editor; store under `data/labels/by_annotator/<id>/` for multi-annotator agreement.
