from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_a1_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/unitree_a1/a1_ros1_pkg_2026-04-25/robot.urdf"
    data = ex.extract(urdf, "unitree_a1")
    assert data["robot_family"] == "unitree_a1"
    assert data["robot_name_urdf"] == "a1"
    assert data["counts"]["links"] == 23
    assert data["counts"]["joints"] == 22
    assert data["counts"]["actuated_joints"] == 12
    assert data["flags"]["has_gripper_joint"] is False
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/") and m.lower().endswith(".dae") for m in meshes)
    assert "meshes/trunk.dae" in meshes
