from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.amd_demo import run_amd_explanation
from app.inference import amd_configured
from app.relic import continuity_snapshot, evaluate_case

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "data" / "demo-company" / "policies.json"
DEMO_PATH = ROOT / "app" / "static" / "index.html"

app = FastAPI(
    title="ReLiC AMD Business Continuity",
    version="0.4.0",
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
        "runecore": "authority-continuity-scaffold",
        "continuity": continuity_snapshot(),
        "amd_vllm_configured": amd_configured(),
        "amd_tokenfactory_execution_evidence": "PASS",
        "direct_hip_rocm_parity": "UNTESTED",
        "warning": (
            "TokenFactory execution has controlled sentinel evidence. "
            "Direct MI300X/HIP/ROCm parity is not claimed."
        ),
    }


@app.get("/continuity")
def continuity() -> dict:
    return continuity_snapshot()


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


@app.post("/decision/amd-explain")
def decision_amd_explain(case: RefundCase) -> dict:
    if not amd_configured():
        raise HTTPException(status_code=503, detail="AMD TokenFactory endpoint is not configured")

    result = evaluate_case(case.amount, case.customer_tier, case.enterprise_plus_active)
    case_data = case.model_dump()
    decision_data = result.as_dict()

    try:
        explanation = run_amd_explanation(case_data, decision_data)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=502, detail=f"AMD output failed deterministic validation: {exc}") from exc

    return {
        "case": case_data,
        "decision": decision_data,
        "inference_mode": "amd-tokenfactory-bounded-explanation",
        "amd": explanation.as_dict(),
        "proof_boundary": {
            "deterministic_decision_authoritative": True,
            "model_output_is_canon": False,
            "direct_hip_rocm_parity": "UNTESTED",
        },
    }
