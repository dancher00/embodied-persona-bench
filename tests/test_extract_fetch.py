from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_fetch_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/fetch/fetch_ros_d22b98f/robot.urdf"
    data = ex.extract(urdf, "fetch")
    assert data["robot_family"] == "fetch"
    assert data["robot_name_urdf"] == "fetch"
    assert data["counts"]["links"] == 26
    assert data["counts"]["joints"] == 25
    assert data["counts"]["actuated_joints"] == 15
    assert data["flags"]["has_gripper_joint"] is True
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/") for m in meshes)
    assert "meshes/base_link.dae" in meshes
    assert "meshes/base_link_collision.STL" in meshes
