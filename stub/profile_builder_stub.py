"""
Stub profile-builder for the Full-Stack take-home.

Simulates the slow, varying-trust service the real product would call: given a
ticker, it "builds" a public-company profile over ~40s and returns fields that
deliberately include LOW-CONFIDENCE, CONFLICTING, MISSING, NEWS-sourced, and
long values — so candidates can build the async job UX + the trust-aware review
UI without ever touching SEC filings or AI.

Run:
    pip install fastapi uvicorn
    uvicorn profile_builder_stub:app --reload --port 9000
    # tip: BUILD_SECONDS=8 uvicorn ...   # speed up local iteration

Contract:
    POST /build           {"ticker": "XYZ"}   -> {"job_id": "..."}
    GET  /build/{job_id}                       -> {"status", "progress", "profile?", "error?"}
        status:   "running" | "done" | "failed"
        progress: 0..100
        profile:  [field, ...]  (present only once status == "done")

Field shapes (the UI must handle ALL of these):
    normal:        {section, field, label, value, source, source_url, confidence}
    news-sourced:  ...as normal, plus source_date  (lower trust than filings)
    low-confidence: confidence < ~0.6  -> surface for review, don't auto-accept
    missing:       value=null, confidence=0, note="..."
    conflict:      {section, field, label, conflict: true,
                    candidates: [{value, source, source_url, confidence}, ...]}

Special tickers:
    FAILCO   -> the build FAILS partway (test failure + retry, don't lose accepted fields)
    <other>  -> succeeds with a realistic profile (ticker echoed into the data)
    ""       -> 400
"""
import os
import time
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Profile Builder Stub")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

BUILD_SECONDS = float(os.environ.get("BUILD_SECONDS", "40"))  # how long a build takes
_jobs: dict = {}  # job_id -> {ticker, started, fail}

_SEC = "https://www.sec.gov/cgi-bin/browse-edgar"  # placeholder source_url


def _profile(ticker: str):
    t = ticker.upper()
    return [
        {"section": "Identity", "field": "company_legal_name", "label": "Legal name",
         "value": f"{t} Holdings, Inc.", "source": "10-K filed 2026-02-20", "source_url": _SEC, "confidence": 0.99},
        {"section": "Identity", "field": "ticker", "label": "Ticker",
         "value": t, "source": "SEC EDGAR", "source_url": _SEC, "confidence": 1.0},
        {"section": "Identity", "field": "exchange", "label": "Exchange",
         "value": "NASDAQ", "source": "10-K filed 2026-02-20", "source_url": _SEC, "confidence": 0.95},
        {"section": "Business", "field": "description", "label": "What they do",
         "value": "Designs and sells industrial IoT sensors and the analytics platform that turns the sensor data into uptime and energy-efficiency recommendations for mid-market manufacturers.",
         "source": "10-K Item 1", "source_url": _SEC, "confidence": 0.9},
        {"section": "Business", "field": "segments", "label": "Segments",
         "value": "Hardware (62% of revenue), Software & Services (38%)", "source": "10-K Item 7 (MD&A)", "source_url": _SEC, "confidence": 0.85},
        {"section": "Financials", "field": "revenue_ttm", "label": "Revenue (TTM)",
         "value": "$48.2M", "source": "10-Q filed 2026-05-10", "source_url": _SEC, "confidence": 0.95},
        {"section": "Financials", "field": "revenue_growth_yoy", "label": "Revenue growth (YoY)",
         "value": "+27%", "source": "derived from 10-Q + 10-K", "source_url": _SEC, "confidence": 0.8},
        {"section": "Financials", "field": "gross_margin", "label": "Gross margin",
         "value": "61%", "source": "10-Q filed 2026-05-10", "source_url": _SEC, "confidence": 0.9},
        {"section": "Financials", "field": "cash", "label": "Cash & equivalents",
         "value": "$31.0M", "source": "10-Q filed 2026-05-10", "source_url": _SEC, "confidence": 0.95},
        {"section": "Financials", "field": "net_income_ttm", "label": "Net income (TTM)",
         "value": "-$6.4M", "source": "10-Q filed 2026-05-10", "source_url": _SEC, "confidence": 0.9},

        # --- CONFLICT: two filings disagree on the share count ---
        {"section": "Capital", "field": "shares_outstanding", "label": "Shares outstanding",
         "conflict": True, "candidates": [
             {"value": "112.4M", "source": "10-Q filed 2026-05-10", "source_url": _SEC, "confidence": 0.9},
             {"value": "115.0M", "source": "8-K filed 2026-06-01 (post-raise)", "source_url": _SEC, "confidence": 0.75},
         ]},
        {"section": "Capital", "field": "recent_raise", "label": "Recent raise",
         "value": "$12M registered direct offering, priced 2026-05-29", "source": "8-K filed 2026-05-30", "source_url": _SEC, "confidence": 0.92},

        # --- LOW CONFIDENCE (surface for review, don't auto-accept) ---
        {"section": "Capital", "field": "shelf_capacity", "label": "Active shelf (S-3) remaining",
         "value": "~$40M (estimated)", "source": "S-3 filed 2025-09-15", "source_url": _SEC, "confidence": 0.45},
        {"section": "Business", "field": "tam", "label": "Market size (TAM)",
         "value": "~$8B (management estimate)", "source": "Investor presentation (8-K Ex. 99)", "source_url": _SEC, "confidence": 0.4},

        # --- MISSING (not disclosed) ---
        {"section": "Financials", "field": "free_cash_flow", "label": "Free cash flow",
         "value": None, "confidence": 0.0, "note": "not separately disclosed in the latest filings"},

        # --- NEWS-sourced (lower trust than a filing; carries a date) ---
        {"section": "Catalysts", "field": "latest_catalyst", "label": "Recent catalyst",
         "value": "Raised FY guidance on 2026-05-28 citing data-center demand", "source": "Reuters",
         "source_url": "https://www.reuters.com/", "source_date": "2026-05-28", "confidence": 0.7},

        # --- deliberately LONG value (stress the layout) ---
        {"section": "Risks", "field": "top_risk", "label": "Top risk factor",
         "value": "Customer concentration: the two largest customers represented approximately 41% of revenue in the most recent fiscal year; the loss of either, or a material reduction in their orders, would have a disproportionate effect on results, and the underlying contracts are generally cancelable by the customer on 30 days' notice.",
         "source": "10-K Item 1A", "source_url": _SEC, "confidence": 0.88},
    ]


class BuildReq(BaseModel):
    ticker: str


@app.post("/build")
def build(req: BuildReq):
    ticker = (req.ticker or "").strip()
    if not ticker:
        raise HTTPException(400, "ticker is required")
    job_id = uuid.uuid4().hex[:12]
    _jobs[job_id] = {"ticker": ticker, "started": time.time(), "fail": ticker.upper() == "FAILCO"}
    return {"job_id": job_id}


@app.get("/build/{job_id}")
def status(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(404, "unknown job_id")
    elapsed = time.time() - job["started"]
    progress = min(100, int(elapsed / BUILD_SECONDS * 100))
    # FAILCO fails about halfway through.
    if job["fail"] and elapsed > BUILD_SECONDS * 0.5:
        return {"status": "failed", "progress": progress,
                "error": "Upstream filing fetch failed (simulated). Please retry."}
    if progress < 100:
        return {"status": "running", "progress": progress}
    return {"status": "done", "progress": 100, "profile": _profile(job["ticker"])}
