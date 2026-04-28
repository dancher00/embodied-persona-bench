from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_pepper_jrl_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/pepper/jrl_b953b44/robot.urdf"
    data = ex.extract(urdf, "pepper")
    assert data["robot_family"] == "pepper"
    assert data["robot_name_urdf"] == "pepper"
    assert data["counts"]["links"] == 65
    assert data["counts"]["joints"] == 64
    assert data["counts"]["actuated_joints"] == 45
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/") for m in meshes)
    assert "meshes/HeadYaw.dae" in meshes
