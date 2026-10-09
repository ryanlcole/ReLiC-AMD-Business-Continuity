from __future__ import annotations

import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.inference import amd_configured
from app.relic import evaluate_case

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "data" / "demo-company" / "policies.json"
DEMO_PATH = ROOT / "app" / "static" / "index.html"

app = FastAPI(
    title="ReLiC AMD Business Continuity",
    version="0.2.0",
    description="Provenance-aware business decision continuity prototype.",
)


class RefundCase(BaseModel):
    amount: float = Field(gt=0)
    customer_tier: str
    enterprise_plus_active: bool = False


@app.get("/")
def root() -> FileResponse:
    return FileResponse(DEMO_PATH)


@app.get("/status")
def status() -> dict:
    return {
        "product": "ReLiC AMD Business Continuity",
        "status": "hackathon-mvp",
        "amd_vllm_configured": amd_configured(),
        "warning": "AMD execution is not claimed until the event endpoint is configured and verified.",
    }


@app.get("/evidence")
def evidence() -> list[dict]:
    with POLICY_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@app.post("/decision")
def decision(case: RefundCase) -> dict:
    result = evaluate_case(case.amount, case.customer_tier, case.enterprise_plus_active)
    return {
        "case": case.model_dump(),
        "decision": result.as_dict(),
        "inference_mode": "deterministic-local-reference",
        "amd_vllm_configured": amd_configured(),
    }
