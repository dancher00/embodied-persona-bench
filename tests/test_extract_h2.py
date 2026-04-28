from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_unitree_h2_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/unitree_h2/unitree_ros_202c598/robot.urdf"
    data = ex.extract(urdf, "unitree_h2")
    assert data["robot_family"] == "unitree_h2"
    assert data["robot_name_urdf"] == "H2"
    assert data["counts"]["links"] == 32
    assert data["counts"]["joints"] == 31
    assert data["counts"]["actuated_joints"] == 31
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/") and m.lower().endswith(".stl") for m in meshes)
    assert "meshes/pelvis.stl" in meshes
