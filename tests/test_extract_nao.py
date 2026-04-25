from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_nao_jrl_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/nao/jrl_v40_6f4e94b/robot.urdf"
    data = ex.extract(urdf, "nao")
    assert data["robot_family"] == "nao"
    assert data["robot_name_urdf"] == "NAOV40"
    assert data["counts"]["links"] == 84
    assert data["counts"]["joints"] == 83
    assert data["counts"]["actuated_joints"] == 42
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/V40/") for m in meshes)
    assert "meshes/V40/Torso.dae" in meshes
