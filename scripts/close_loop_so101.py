#!/usr/bin/env python3
"""One command: embodiment.json → preview render → validate pilot label paths exist."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    snap = root / "data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9"
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=root)
    args = p.parse_args()
    root = args.root
    snap = root / "data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9"
    urdf = snap / "robot.urdf"
    emb = snap / "embodiment.json"
    mesh_dir = snap / "meshes"
    render = root / "data/renders/so101_brukg_5e97ca9/preview.png"
    label = root / "data/labels/so101_brukg_5e97ca9.placeholder.json"

    if not urdf.is_file():
        print(f"error: missing {urdf}", file=sys.stderr)
        return 1

    subprocess.run(
        [
            sys.executable,
            str(root / "scripts/extract_urdf_features.py"),
            "--urdf",
            str(urdf),
            "--robot-family",
            "so_101",
            "--out",
            str(emb),
        ],
        check=True,
    )

    digest = json.loads(emb.read_text(encoding="utf-8"))["urdf_digest"]
    label_data = json.loads(label.read_text(encoding="utf-8"))
    label_data["urdf_digest"] = digest
    label.write_text(
        json.dumps(label_data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            str(root / "scripts/render_meshes_preview.py"),
            "--mesh-dir",
            str(mesh_dir),
            "--out",
            str(render),
            "--title",
            "so101_brukg_5e97ca9 (preview point cloud)",
        ],
        check=True,
    )

    subprocess.run(
        [
            sys.executable,
            str(root / "scripts/validate_label.py"),
            str(label),
        ],
        check=True,
        cwd=str(root),
    )

    print("OK closed loop:")
    print(" ", emb)
    print(" ", render)
    print(" ", label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
