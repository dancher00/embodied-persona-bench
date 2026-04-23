# Data directory

Large binaries **do not** belong in git.

Planned layout (local or release archive):

```
data/
  urdf_snapshots/     # versioned URDF + meshes; record sha256 in manifest
  renders/            # PNGs shown to annotators
  labels/             # JSON lines, one label per file or consolidated with split column
  manifest.csv        # sample_id, robot_family, urdf_path, render_path, split
```

For NeurIPS Evaluations & Datasets track, the public release will be hosted on a designated platform (e.g. Hugging Face) with **Croissant** metadata (core + Responsible AI fields).

## Robot families (v0)

| `robot_family`   | Notes |
|------------------|--------|
| `unitree_a1`     | Quadruped snapshot you pin in the manifest |
| `turtlebot3_burger` | Differential drive |
| `xlerobot`       | Pin exact hardware revision / URDF package version |
| `so_101`         | Pin exact arm configuration |

Record provenance (upstream repo URL + commit or ROS package version) in `manifest.csv` or dataset card.
