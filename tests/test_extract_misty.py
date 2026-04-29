from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_misty_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/misty/misty_ros_74b5706/robot.urdf"
    data = ex.extract(urdf, "misty")
    assert data["robot_family"] == "misty"
    assert data["robot_name_urdf"] == "misty"
    assert data["counts"]["links"] == 27
    assert data["counts"]["joints"] == 26
    assert data["counts"]["actuated_joints"] == 9
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/") and m.lower().endswith(".stl") for m in meshes)
    assert "meshes/base_link.stl" in meshes
