# SO-100 5-DOF — flat snapshot (kinematics only)

Upstream: [brukg/SO-100-arm](https://github.com/brukg/SO-100-arm) @ `5e97ca9`.

## Layout

```text
robot.urdf       # plain URDF (no xacro, no ros2_control)
meshes/*.STL     # collision/visual meshes
PROVENANCE.txt
LICENSE.upstream
```

Mesh `filename` entries in `robot.urdf` are **relative to this folder** (`meshes/Base.STL`, …).

## Regenerate (after updating upstream copy)

`scripts/emit_so100_flat_urdf.py` expects a **temporary** tree with:

- `urdf/so_arm_100_5dof_arm.urdf.xacro`
- `models/so_arm_100_5dof/meshes/*.STL`

Copy those paths out of `so_arm_100_description/` from the upstream repo, then:

```bash
python3 scripts/emit_so100_flat_urdf.py --snapshot data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9 --prune
```

`--prune` deletes the `urdf/` and `models/` trees after emitting (keeps only `robot.urdf` + `meshes/`).

## License

Apache-2.0 — see `LICENSE.upstream`.
