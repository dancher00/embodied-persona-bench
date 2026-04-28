# Where to put URDF files

Put each **versioned snapshot** under its robot family. One snapshot = one folder.

## Layout

```text
data/urdf_snapshots/
  <robot_family>/
    <snapshot_id>/
      robot.urdf          # REQUIRED: top-level URDF (xacro must be expanded to .urdf first)
      meshes/             # optional: collision/visual meshes referenced by robot.urdf
      package.xml         # optional: if you copy a whole ROS package for provenance
      PROVENANCE.txt      # REQUIRED: upstream URL, version/tag/commit, license note
```

## `robot_family` (folder name = schema enum)

Use **exactly** these directory names (match `schema/persona_label.schema.json`):

| Folder name           | Robot |
|-----------------------|--------|
| `unitree_a1`          | Unitree A1 |
| `unitree_r1`         | Unitree R1 (humanoid) |
| `unitree_h2`         | Unitree H2 (humanoid) |
| `turtlebot3_burger`   | TurtleBot3 Burger |
| `xlerobot`            | XLeRobot |
| `so_101`              | SO-101 |
| `nao`                 | SoftBank / Aldebaran NAO (humanoid) |

## `snapshot_id` (your version label)

Short, unique, no spaces. Examples:

- `official_humble_2026-04-24`
- `unitree_ros2_commit_abc12def`
- `my_lab_baseline_v0`

Rules:

- Use **only** `[a-z0-9_-]` (lowercase).
- Prefer **date** or **upstream git commit** in the name so you can tell snapshots apart.

## Canonical file name

- Prefer a single entry file **`robot.urdf`** (plain URDF) inside `<snapshot_id>/`, with **`meshes/`** next to it if STL paths are relative (`meshes/link.stl`). Example: `so_101/brukg_SO-100-arm_5e97ca9/`.
- If you only keep **xacro**, use **`urdf/robot.urdf.xacro`** as the entry and document how to expand to `robot.urdf`.
- If upstream uses another basename, still expose **`robot.urdf`** or **`robot.urdf.xacro`** as the canonical entry for tooling.

## Meshes

- Keep relative paths from `robot.urdf` valid: usually a `meshes/` subfolder next to `robot.urdf`.
- If upstream spreads files across many dirs, mirror that structure under the same `<snapshot_id>/` root.
- **Collada (`.dae`)** often references sidecar images (e.g. `trunk_A1.png` next to `trunk.dae`). Copy those files too, or the browser viewer will 404 on textures while geometry still loads.

## After you add files

1. Copy `PROVENANCE.template.txt` to `PROVENANCE.txt` inside the same `<snapshot_id>/` folder and fill it in.
2. Run `python scripts/extract_urdf_features.py --urdf .../robot.urdf --out .../embodiment.json` (once implemented) and record the `urdf_digest` in your label or manifest row.

### Git note (this repository)

Small **curated** snapshots (xacro + STL + `PROVENANCE.txt`) under `data/urdf_snapshots/` are **tracked**. Nested vendor `.git/` trees under `data/` are ignored—clone upstream elsewhere, then copy a pruned snapshot here (see `so_101/brukg_SO-100-arm_*`).

### `PROVENANCE.txt` template

```text
upstream_url: <https://...>
upstream_version: <tag / ROS distro / package version>
license: <e.g. BSD-3-Clause>
retrieved_date: <YYYY-MM-DD>
notes: <optional: what you changed vs upstream>
```
