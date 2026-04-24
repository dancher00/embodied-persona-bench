# Data directory

Large binaries **do not** belong in git.

Planned layout (local or release archive):

```text
data/
  urdf_snapshots/     # see urdf_snapshots/NAMING.md — where to copy official URDFs
  renders/            # PNGs shown to annotators
  labels/             # JSON lines, one label per file or consolidated with split column
  manifest.csv        # copy from manifest.example.csv when ready; URDF + embodiment.json + split
```

**URDF drop-in guide:** `data/urdf_snapshots/NAMING.md`  
**SO-101 / SO-100 sample:** `data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9/` — `robot.urdf`, `meshes/`, `embodiment.json` (from `scripts/extract_urdf_features.py`). Row template: `data/manifest.example.csv`.

For NeurIPS Evaluations & Datasets track, the public release will be hosted on a designated platform (e.g. Hugging Face) with **Croissant** metadata (core + Responsible AI fields).

## Robot families (v0)

| `robot_family`   | Notes |
|------------------|--------|
| `unitree_a1`     | Quadruped snapshot you pin in the manifest |
| `turtlebot3_burger` | Differential drive |
| `xlerobot`       | Pin exact hardware revision / URDF package version |
| `so_101`         | SO-100/SO-101 arm (flat URDF + meshes); see `brukg_SO-100-arm_5e97ca9/` |

Record provenance (upstream repo URL + commit or ROS package version) in `manifest.csv` or dataset card.
