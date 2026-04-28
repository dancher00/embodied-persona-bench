from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_unitree_r1_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/unitree_r1/unitree_ros_202c598/robot.urdf"
    data = ex.extract(urdf, "unitree_r1")
    assert data["robot_family"] == "unitree_r1"
    assert data["robot_name_urdf"] == "R1"
    assert data["counts"]["links"] == 40
    assert data["counts"]["joints"] == 39
    assert data["counts"]["actuated_joints"] == 26
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/") and m.lower().endswith((".stl", ".STL")) for m in meshes)
    assert "meshes/pelvis_link.STL" in meshes
