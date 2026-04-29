from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_pr2_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/pr2/pr2_common_9a8e4fb/robot.urdf"
    data = ex.extract(urdf, "pr2")
    assert data["robot_family"] == "pr2"
    assert data["robot_name_urdf"] == "pr2"
    assert data["counts"]["links"] == 88
    assert data["counts"]["joints"] == 87
    assert data["counts"]["actuated_joints"] == 45
    assert data["flags"]["has_gripper_joint"] is True
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    meshes = data["mesh_filenames"]
    assert all(m.startswith("meshes/") for m in meshes)
    assert "meshes/base_v0/base.dae" in meshes
    assert "meshes/torso_v0/torso_lift.dae" in meshes
