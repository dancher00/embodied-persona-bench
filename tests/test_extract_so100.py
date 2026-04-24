from __future__ import annotations

from pathlib import Path

import extract_urdf_features as ex


def test_extract_so100_snapshot() -> None:
    root = Path(__file__).resolve().parents[1]
    urdf = root / "data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9/robot.urdf"
    data = ex.extract(urdf, "so_101")
    assert data["robot_family"] == "so_101"
    assert data["robot_name_urdf"] == "so_arm_100_5dof"
    assert data["counts"]["links"] == 9
    assert data["counts"]["joints"] == 8
    assert data["counts"]["actuated_joints"] == 6
    assert data["flags"]["has_gripper_joint"] is True
    assert data["mesh_files_missing"] == []
    assert len(data["urdf_digest"]) == 64
    jnames = [j["name"] for j in data["joints"]]
    assert "Gripper" in jnames
    assert "Elbow" in jnames
