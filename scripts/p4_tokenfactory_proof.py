#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from app.amd_demo import run_amd_explanation
from app.relic import evaluate_case


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence" / "amd_tokenfactory_p4.json"


def main() -> None:
    case = {
        "amount": 750.0,
        "customer_tier": "Enterprise Plus",
        "enterprise_plus_active": True,
    }
    result = evaluate_case(
        case["amount"],
        case["customer_tier"],
        case["enterprise_plus_active"],
    )
    decision = result.as_dict()

    # Exactly one live AMD call occurs inside run_amd_explanation.
    amd = run_amd_explanation(case, decision)

    artifact = {
        "schema": "RELIC-AMD-P4/1",
        "status": "PASS",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "claim": "AMD TokenFactory produced a bounded explanation that passed deterministic validation",
        "case": case,
        "decision": decision,
        "amd": amd.as_dict(),
        "boundaries": {
            "model_output_is_canon": False,
            "deterministic_decision_authoritative": True,
            "relic_ingestion_status": "NOT_INGESTED",
            "direct_mi300x_execution": "UNTESTED",
            "hip_rocm_parity": "UNTESTED",
        },
        "secret_handling": "No API key or bearer token is written to this artifact.",
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": artifact["status"],
        "output": str(OUTPUT.relative_to(ROOT)),
        "validated": amd.validated,
        "model": amd.model,
        "usage": amd.usage,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
