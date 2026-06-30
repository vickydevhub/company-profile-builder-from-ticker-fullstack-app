# Stub Profile-Builder — for the Full-Stack take-home

This simulates the real "build a public-company profile from a ticker" service, so you can build
the **product layer** (async job UX + the review UI) **without touching SEC filings or AI.**

## Run
```bash
pip install fastapi uvicorn
uvicorn profile_builder_stub:app --reload --port 9000
# tip: speed up local iteration ->  BUILD_SECONDS=8 uvicorn profile_builder_stub:app --port 9000
```

## Contract
- `POST /build` `{"ticker": "XYZ"}` → `{"job_id": "..."}`
- `GET /build/{job_id}` → `{"status", "progress", "profile?", "error?"}`
  - `status`: `running` | `done` | `failed`
  - `progress`: `0–100`
  - `profile`: present **only** when `status == "done"` — a list of fields.

The build takes ~40s on purpose. Don't block the UI on it.

## Field shapes — your UI must handle all of these
- **Normal:** `{section, field, label, value, source, source_url, confidence}`
- **News-sourced** (lower trust than a filing): same, plus `source_date`.
- **Low confidence:** `confidence` below ~0.6 → surface it for review, don't silently accept.
- **Missing:** `value: null`, `confidence: 0`, plus a `note`.
- **Conflict:** `{section, field, label, conflict: true, candidates: [{value, source, source_url, confidence}, …]}` → let the user pick a value.

## Test tickers
- **Any ticker** → succeeds with a realistic profile that includes a conflict, low-confidence
  fields, a missing field, a news-sourced field, and a deliberately long value.
- **`FAILCO`** → the build **fails partway** — test failure handling + retry, and don't lose the
  fields the user already accepted.
- **empty ticker** → `400`.
