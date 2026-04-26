#!/usr/bin/env python3
"""Minimal ratings API backed by SQLite for annotation prototype."""

from __future__ import annotations

import json
import sqlite3
from io import StringIO
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import csv

import jsonschema
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schema" / "persona_label.schema.json"
DB_PATH = REPO_ROOT / "data" / "ratings.sqlite3"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def ensure_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id TEXT NOT NULL,
            annotator_id TEXT NOT NULL,
            robot_family TEXT NOT NULL,
            urdf_digest TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS uq_ratings_annotator_sample "
        "ON ratings(annotator_id, sample_id)"
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ratings_sample_id ON ratings(sample_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ratings_annotator ON ratings(annotator_id)")
    conn.commit()


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    ensure_db(conn)
    return conn


class RatingIn(BaseModel):
    annotator_id: str = Field(min_length=1, max_length=48)
    label: dict[str, Any]


app = FastAPI(title="Embodied Persona Ratings API", version="0.1.0")
SCHEMA = load_schema()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "time_utc": utc_now_iso()}


@app.post("/ratings")
def create_rating(payload: RatingIn) -> dict[str, Any]:
    annotator = payload.annotator_id.strip().lower()
    if not annotator or not all(c.isalnum() or c in "_-" for c in annotator):
        raise HTTPException(status_code=400, detail="invalid annotator_id")

    label = payload.label
    try:
        jsonschema.validate(instance=label, schema=SCHEMA)
    except jsonschema.ValidationError as err:
        raise HTTPException(status_code=400, detail=f"schema validation failed: {err.message}") from err

    created_at = utc_now_iso()
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO ratings (
                sample_id,
                annotator_id,
                robot_family,
                urdf_digest,
                payload_json,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(annotator_id, sample_id) DO UPDATE SET
                robot_family = excluded.robot_family,
                urdf_digest = excluded.urdf_digest,
                payload_json = excluded.payload_json,
                created_at = excluded.created_at
            """,
            (
                label["sample_id"],
                annotator,
                label["robot_family"],
                label["urdf_digest"],
                json.dumps(label, sort_keys=True),
                created_at,
            ),
        )
        row = conn.execute(
            "SELECT id FROM ratings WHERE annotator_id = ? AND sample_id = ?",
            (annotator, label["sample_id"]),
        ).fetchone()
        rating_id = row[0] if row else None
        conn.commit()

    return {"ok": True, "id": rating_id, "created_at": created_at}


@app.get("/ratings")
def list_ratings(limit: int = 100, sample_id: str | None = None) -> dict[str, Any]:
    safe_limit = max(1, min(limit, 1000))
    query = (
        "SELECT id, sample_id, annotator_id, robot_family, urdf_digest, created_at, payload_json "
        "FROM ratings"
    )
    params: list[Any] = []
    if sample_id:
        query += " WHERE sample_id = ?"
        params.append(sample_id)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(safe_limit)

    with get_connection() as conn:
        rows = conn.execute(query, tuple(params)).fetchall()

    items: list[dict[str, Any]] = []
    for row in rows:
        items.append(
            {
                "id": row[0],
                "sample_id": row[1],
                "annotator_id": row[2],
                "robot_family": row[3],
                "urdf_digest": row[4],
                "created_at": row[5],
                "label": json.loads(row[6]),
            }
        )
    return {"count": len(items), "items": items}


@app.get("/ratings.csv", response_class=PlainTextResponse)
def export_ratings_csv(sample_id: str | None = None) -> str:
    query = (
        "SELECT id, sample_id, annotator_id, robot_family, urdf_digest, created_at, payload_json "
        "FROM ratings"
    )
    params: list[Any] = []
    if sample_id:
        query += " WHERE sample_id = ?"
        params.append(sample_id)
    query += " ORDER BY created_at DESC"

    with get_connection() as conn:
        rows = conn.execute(query, tuple(params)).fetchall()

    out = StringIO()
    writer = csv.writer(out)
    writer.writerow(
        ["id", "sample_id", "annotator_id", "robot_family", "urdf_digest", "created_at", "payload_json"]
    )
    for row in rows:
        writer.writerow(list(row))
    return out.getvalue()
