from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_lekiwi_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/lekiwi/sig_uiuc_f93df541/robot.urdf"
    data = ex.extract(urdf, "lekiwi")
    assert data["robot_family"] == "lekiwi"
    assert data["robot_name_urdf"] == "LeKiwi"
    assert data["counts"]["links"] == 45
    assert data["counts"]["joints"] == 44
    assert data["counts"]["actuated_joints"] == 9
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/") and m.lower().endswith(".stl") for m in meshes)
    assert "meshes/base_plate_layer1-v5.stl" in meshes
