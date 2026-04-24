#!/usr/bin/env python3
"""Extract an embodiment summary from a plain URDF (stdlib XML; no ROS required)."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


def _digest_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _mesh_paths(urdf_dir: Path, root: ET.Element) -> list[str]:
    out: list[str] = []
    for mesh in root.iter("mesh"):
        fn = mesh.attrib.get("filename")
        if fn:
            out.append(fn)
    return sorted(set(out))


def _missing_meshes(urdf_dir: Path, mesh_filenames: list[str]) -> list[str]:
    missing: list[str] = []
    for rel in mesh_filenames:
        p = urdf_dir / rel
        if not p.is_file():
            missing.append(rel)
    return missing


def extract(urdf_path: Path, robot_family: str | None) -> dict:
    root = ET.parse(urdf_path).getroot()
    if root.tag != "robot":
        raise ValueError(f"expected <robot> root, got <{root.tag}>")

    robot_name = root.attrib.get("name", "")
    urdf_dir = urdf_path.resolve().parent
    mesh_refs = _mesh_paths(urdf_dir, root)

    links = [el.attrib["name"] for el in root.findall("link") if "name" in el.attrib]
    joints: list[dict] = []
    for j in root.findall("joint"):
        name = j.attrib.get("name", "")
        jtype = j.attrib.get("type", "")
        parent_el = j.find("parent")
        child_el = j.find("child")
        parent = parent_el.attrib.get("link") if parent_el is not None else None
        child = child_el.attrib.get("link") if child_el is not None else None
        axis_el = j.find("axis")
        axis = None
        if axis_el is not None and "xyz" in axis_el.attrib:
            axis = axis_el.attrib["xyz"]
        lim = j.find("limit")
        limits = None
        if lim is not None:
            limits = {
                "lower": lim.attrib.get("lower"),
                "upper": lim.attrib.get("upper"),
                "effort": lim.attrib.get("effort"),
                "velocity": lim.attrib.get("velocity"),
            }
        joints.append(
            {
                "name": name,
                "type": jtype,
                "parent": parent,
                "child": child,
                "axis_xyz": axis,
                "limit": limits,
            }
        )

    type_counts = Counter(j["type"] for j in joints)
    actuated_types = {"revolute", "continuous", "prismatic"}
    n_actuated = sum(1 for j in joints if j["type"] in actuated_types)

    has_gripper_joint = any(
        j["type"] in actuated_types and "gripper" in j["name"].lower() for j in joints
    )
    has_end_effector_link = any("end_effector" in ln.lower() for ln in links)

    mobility = "manipulator"
    if any(t in type_counts for t in ("floating", "planar")):
        mobility = "floating_or_planar_base"
    elif type_counts.get("fixed", 0) >= 1 and n_actuated >= 1:
        mobility = "manipulator"

    family = robot_family
    if not family:
        family = "unknown"

    missing = _missing_meshes(urdf_dir, mesh_refs)

    return {
        "schema_version": "0.1.0",
        "robot_family": family,
        "robot_name_urdf": robot_name,
        "urdf_path": str(urdf_path),
        "urdf_digest": _digest_file(urdf_path),
        "counts": {
            "links": len(links),
            "joints": len(joints),
            "actuated_joints": n_actuated,
            "joint_types": dict(type_counts),
        },
        "link_names": links,
        "joints": joints,
        "mobility_class": mobility,
        "flags": {
            "has_gripper_joint": has_gripper_joint,
            "has_end_effector_link": has_end_effector_link,
        },
        "mesh_filenames": mesh_refs,
        "mesh_files_missing": missing,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="URDF → embodiment summary JSON")
    p.add_argument("--urdf", type=Path, required=True, help="Path to robot.urdf")
    p.add_argument("--robot-family", type=str, default=None, help="e.g. so_101 (stored in JSON)")
    p.add_argument("--out", type=Path, help="Write JSON summary to this path")
    args = p.parse_args()

    if not args.urdf.is_file():
        print(f"error: not a file: {args.urdf}", file=sys.stderr)
        return 1

    try:
        summary = extract(args.urdf, args.robot_family)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if summary["mesh_files_missing"]:
        print(
            "warning: missing mesh files (paths relative to URDF directory): "
            + ", ".join(summary["mesh_files_missing"]),
            file=sys.stderr,
        )

    text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
