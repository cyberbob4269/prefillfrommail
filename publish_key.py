"""Publish PrefillFromMail unlock JSON to GitHub Pages repo (no Cloudflare)."""
from __future__ import annotations

import base64
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO = "cyberbob4269/prefillfrommail"
SITE = Path(r"C:\Users\TSLA BoT\Documents\FieldOps\google\commercial\unlock-site")


def gh_api(method: str, path: str, body: dict | None = None) -> dict[str, Any]:
    cmd = ["gh", "api", "-X", method, path]
    if body is not None:
        cmd.extend(["--input", "-"])
    proc = subprocess.run(
        cmd,
        input=json.dumps(body).encode() if body is not None else None,
        capture_output=True,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout).decode("utf-8", errors="replace")
        raise RuntimeError(f"gh api {method} {path} failed: {err}")
    raw = proc.stdout.decode("utf-8", errors="replace").strip()
    return json.loads(raw) if raw else {}


def put_file(path: str, content: str, message: str) -> None:
    """Create or update a file in REPO via Contents API."""
    api_path = f"repos/{REPO}/contents/{path}"
    existing_sha = None
    try:
        existing = gh_api("GET", api_path)
        existing_sha = existing.get("sha")
    except RuntimeError:
        existing_sha = None
    payload: dict[str, Any] = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch": "main",
    }
    if existing_sha:
        payload["sha"] = existing_sha
    gh_api("PUT", api_path, payload)


def publish_license(rec: dict[str, Any]) -> None:
    session_id = str(rec.get("session_id") or "")
    key = str(rec.get("key") or "")
    if not session_id or not key:
        raise ValueError("session_id and key required")
    body = {
        "ok": True,
        "key": key,
        "tier": rec.get("tier") or "kit",
        "remaining": max(
            0,
            int(rec.get("max_activations") or 3) - len(rec.get("sheet_ids") or []),
        ),
        "max_activations": int(rec.get("max_activations") or 3),
        "sheet_ids": list(rec.get("sheet_ids") or []),
        "make_copy_url": rec.get("make_copy_url")
        or "https://docs.google.com/spreadsheets/d/1BDwhWIu9f1ej_TvVR_z8pU4KLPhSeVfFQAJ0ivqA-qI/copy",
        "session_id": session_id,
        "email": rec.get("email") or "",
    }
    text = json.dumps(body, indent=2) + "\n"
    put_file(
        f"keys/{session_id}.json",
        text,
        f"unlock {session_id[:20]}…",
    )
    # Lookup by key for activation checks
    put_file(
        f"keys/by-key/{key}.json",
        text,
        f"key index {key}",
    )
    print("published", session_id, key)


def publish_from_vera_store(session_id: str | None = None) -> None:
    vera = Path(r"C:\Users\Vera-at-home\projects\vera-home\data\pfm_licenses.json")
    store = json.loads(vera.read_text(encoding="utf-8"))
    by_session = store.get("by_session") or {}
    by_key = store.get("by_key") or {}
    if session_id:
        key = by_session.get(session_id)
        if not key:
            raise SystemExit(f"session not in Vera store: {session_id}")
        publish_license(by_key[key])
        return
    for sid, key in by_session.items():
        publish_license(by_key[key])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        publish_from_vera_store(sys.argv[1])
    else:
        publish_from_vera_store()
