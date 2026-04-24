#!/usr/bin/env python3
"""Emit kinematics-only robot.urdf + copy meshes into a flat snapshot layout.

Requires `urdf/so_arm_100_5dof_arm.urdf.xacro` and `models/so_arm_100_5dof/meshes/`
under the snapshot directory (e.g. copied from upstream `so_arm_100_description`).
After `--prune`, only `robot.urdf` and `meshes/` remain — re-copy from upstream to run again.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def emit(snap: Path) -> None:
    arm_src = snap / "urdf" / "so_arm_100_5dof_arm.urdf.xacro"
    if not arm_src.is_file():
        raise FileNotFoundError(arm_src)
    lines = arm_src.read_text(encoding="utf-8").splitlines()
    body = lines[19:397]
    out: list[str] = ['<?xml version="1.0"?>', '<robot name="so_arm_100_5dof">']
    skip = False
    for line in body:
        if "<gazebo>" in line:
            skip = True
            continue
        if skip:
            if "</gazebo>" in line:
                skip = False
            continue
        line = line.replace("${prefix}", "")
        line = line.replace("${meshes_file_directory}", "meshes")
        out.append(line)
    out.append("</robot>")
    (snap / "robot.urdf").write_text("\n".join(out) + "\n", encoding="utf-8")

    mesh_src = snap / "models" / "so_arm_100_5dof" / "meshes"
    if not mesh_src.is_dir():
        raise FileNotFoundError(mesh_src)
    meshes_dst = snap / "meshes"
    meshes_dst.mkdir(exist_ok=True)
    for f in sorted(mesh_src.glob("*.STL")):
        shutil.copy2(f, meshes_dst / f.name)


def prune_ros_tree(snap: Path) -> None:
    for name in ("urdf", "ros2_control", "models", "_build_flat"):
        p = snap / name
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--snapshot",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9",
    )
    p.add_argument(
        "--prune",
        action="store_true",
        help="Remove urdf/, ros2_control/, models/ after emitting flat files",
    )
    args = p.parse_args()
    snap: Path = args.snapshot
    emit(snap)
    if args.prune:
        prune_ros_tree(snap)
    print("OK", snap / "robot.urdf", snap / "meshes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
