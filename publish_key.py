"""PrefillFromMail license helpers — local Vera store only.

Licenses must NOT be published to the public GitHub Pages repo
(cyberbob4269/prefillfrommail). They live in the private Vera store and are
served by the Cloudflare Worker (FieldOps/google/commercial/unlock-worker,
worker name pfm-unlock).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

VERA_STORE = Path(r"C:\Users\Vera-at-home\projects\vera-home\data\pfm_licenses.json")

_PUBLIC_PUBLISH_MSG = (
    "Refusing to publish license payloads to the public GitHub repo. "
    "Licenses are stored in the private Vera store "
    f"({VERA_STORE}) and served by the Cloudflare Worker "
    "(FieldOps/google/commercial/unlock-worker, worker name pfm-unlock)."
)


def load_vera_store() -> dict[str, Any]:
    """Load the private Vera license store (local only)."""
    return json.loads(VERA_STORE.read_text(encoding="utf-8"))


def license_payload(rec: dict[str, Any]) -> dict[str, Any]:
    """Build the unlock API payload shape from a Vera store record."""
    session_id = str(rec.get("session_id") or "")
    key = str(rec.get("key") or "")
    if not session_id or not key:
        raise ValueError("session_id and key required")
    return {
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


def publish_license(rec: dict[str, Any]) -> None:
    """Hard error — public GitHub publish is disabled."""
    raise RuntimeError(_PUBLIC_PUBLISH_MSG)


def publish_from_vera_store(session_id: str | None = None) -> None:
    """Hard error — public GitHub publish is disabled."""
    raise SystemExit(_PUBLIC_PUBLISH_MSG)


def lookup_license(session_id: str | None = None, key: str | None = None) -> dict[str, Any]:
    """Local-only helper: return unlock payload from the Vera store."""
    store = load_vera_store()
    by_session = store.get("by_session") or {}
    by_key = store.get("by_key") or {}
    if session_id:
        license_key = by_session.get(session_id)
        if not license_key:
            raise SystemExit(f"session not in Vera store: {session_id}")
        return license_payload(by_key[license_key])
    if key:
        rec = by_key.get(key)
        if not rec:
            raise SystemExit(f"key not in Vera store: {key}")
        return license_payload(rec)
    raise SystemExit("provide session_id or key")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        payload = lookup_license(session_id=sys.argv[1])
        print(json.dumps(payload, indent=2))
    else:
        raise SystemExit(_PUBLIC_PUBLISH_MSG)
