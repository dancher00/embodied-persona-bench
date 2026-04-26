#!/usr/bin/env python3
"""Serve repo root over HTTP so the browser URDF viewer can load robot.urdf + meshes.

Uses the same approach as gkjohnson's urdf-loader examples: fetch URDF, resolve mesh
paths relative to the URDF URL (see tools/urdf_viewer/index.html).

Example:
  python scripts/serve_urdf_viewer.py
  # open http://127.0.0.1:8765/tools/urdf_viewer/index.html?urdf=data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9/robot.urdf
"""

from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
import webbrowser
from pathlib import Path


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Allow local tooling (e.g. Streamlit iframe) to load assets."""

    def end_headers(self) -> None:
        # Browsers cache file://-like static pages aggressively; avoid stale URDF viewer JS/HTML.
        clean = self.path.split("?", 1)[0]
        if "tools/urdf_viewer/" in clean and clean.endswith(".html"):
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--directory",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="HTTP root (repository root)",
    )
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--open", action="store_true", help="Open default SO-101 URDF in browser")
    args = p.parse_args()
    root = args.directory.resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")

    handler = functools.partial(CORSRequestHandler, directory=str(root))
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer((args.host, args.port), handler)
    default_rel = "data/urdf_snapshots/so_101/brukg_SO-100-arm_5e97ca9/robot.urdf"
    url = f"http://{args.host}:{args.port}/tools/urdf_viewer/index.html?urdf={default_rel}"
    print(f"Serving {root}")
    print(f"  URDF viewer: {url}")
    print("  Ctrl+C to stop")
    if args.open:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
