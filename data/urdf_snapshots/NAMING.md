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
| `turtlebot3_burger`   | TurtleBot3 Burger |
| `xlerobot`            | XLeRobot |
| `so_101`              | SO-101 |

## `snapshot_id` (your version label)

Short, unique, no spaces. Examples:

- `official_humble_2026-04-24`
- `unitree_ros2_commit_abc12def`
- `my_lab_baseline_v0`

Rules:

- Use **only** `[a-z0-9_-]` (lowercase).
- Prefer **date** or **upstream git commit** in the name so you can tell snapshots apart.

## Canonical file name

- The main description file **must** be named **`robot.urdf`** inside `<snapshot_id>/`.
  - If upstream uses another name (`a1.urdf`, `turtlebot3_burger.urdf`), copy or symlink it to `robot.urdf` for this benchmark.

## Meshes

- Keep relative paths from `robot.urdf` valid: usually a `meshes/` subfolder next to `robot.urdf`.
- If upstream spreads files across many dirs, mirror that structure under the same `<snapshot_id>/` root.

## After you add files

1. Fill `PROVENANCE.txt` (template below).
2. Run `python scripts/extract_urdf_features.py --urdf .../robot.urdf --out .../embodiment.json` (once implemented) and record the `urdf_digest` in your label or manifest row.

### `PROVENANCE.txt` template

```text
upstream_url: <https://...>
upstream_version: <tag / ROS distro / package version>
license: <e.g. BSD-3-Clause>
retrieved_date: <YYYY-MM-DD>
notes: <optional: what you changed vs upstream>
```
