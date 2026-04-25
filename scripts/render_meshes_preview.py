#!/usr/bin/env python3
"""Headless **thumbnail** PNG from STL directory (matplotlib + numpy-stl).

Does not apply URDF joint poses. For correct robot assembly from `robot.urdf` + meshes,
use `tools/urdf_viewer/` + `scripts/serve_urdf_viewer.py` (Three.js + urdf-loader, same stack as
https://gkjohnson.github.io/urdf-loaders/javascript/example/bundle/ ).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from stl import mesh  # noqa: E402


def load_vertices(mesh_dir: Path) -> np.ndarray:
    blocks: list[np.ndarray] = []
    for p in sorted(mesh_dir.glob("*.STL")):
        m = mesh.Mesh.from_file(str(p))
        blocks.append(m.vectors.reshape(-1, 3))
    if not blocks:
        raise FileNotFoundError(f"no STL in {mesh_dir}")
    return np.vstack(blocks)


def main() -> int:
    p = argparse.ArgumentParser(description="STL folder → single preview PNG")
    p.add_argument("--mesh-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--title", type=str, default="")
    p.add_argument("--max-points", type=int, default=12000, help="subsample vertices for speed")
    args = p.parse_args()

    if not args.mesh_dir.is_dir():
        print(f"error: not a directory: {args.mesh_dir}", file=sys.stderr)
        return 1

    v = load_vertices(args.mesh_dir)
    if len(v) > args.max_points:
        idx = np.linspace(0, len(v) - 1, args.max_points, dtype=int)
        v = v[idx]

    fig = plt.figure(figsize=(7, 6), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(v[:, 0], v[:, 1], v[:, 2], s=2, c=v[:, 2], cmap="viridis", alpha=0.85, linewidths=0)
    ax.set_box_aspect(
        (
            float(np.ptp(v[:, 0]) + 1e-9),
            float(np.ptp(v[:, 1]) + 1e-9),
            float(np.ptp(v[:, 2]) + 1e-9),
        )
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    if args.title:
        ax.set_title(args.title, fontsize=10)
    ax.view_init(elev=20, azim=55)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(args.out, bbox_inches="tight")
    plt.close(fig)
    print("wrote", args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
