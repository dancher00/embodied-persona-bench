from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_unitree_h1_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/unitree_h1/unitree_ros_202c598/robot.urdf"
    data = ex.extract(urdf, "unitree_h1")
    assert data["robot_family"] == "unitree_h1"
    assert data["robot_name_urdf"] == "h1_description"
    assert data["counts"]["links"] == 25
    assert data["counts"]["joints"] == 24
    assert data["counts"]["actuated_joints"] == 19
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/") and m.lower().endswith(".dae") for m in meshes)
    assert "meshes/pelvis.dae" in meshes
