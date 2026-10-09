from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "data" / "demo-company" / "policies.json"


@dataclass(frozen=True)
class Decision:
    action: str
    reason: str
    evidence_ids: list[str]
    confidence: float

    def as_dict(self) -> dict:
        return asdict(self)


def load_policies() -> list[dict]:
    with POLICY_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evaluate_case(amount: float, customer_tier: str, enterprise_plus_active: bool) -> Decision:
    """Deterministic reference resolver used before AMD model integration.

    This deliberately keeps evidence and inference separate. The model layer can
    later explain/check this context, while tests retain a stable business oracle.
    """
    policies = load_policies()
    evidence = [record["id"] for record in policies]

    if amount <= 500:
        return Decision(
            action="auto_approve",
            reason="The base policy requires manager approval only for refunds over $500.",
            evidence_ids=["POL-2026-01"],
            confidence=1.0,
        )

    is_active_plus = customer_tier.strip().casefold() == "enterprise plus" and enterprise_plus_active
    if is_active_plus and amount <= 1000:
        return Decision(
            action="auto_approve",
            reason=(
                "The March Enterprise Plus exception applies, and the April correction "
                "confirms that the customer's Enterprise Plus contract must be active."
            ),
            evidence_ids=evidence,
            confidence=1.0,
        )

    return Decision(
        action="manager_approval",
        reason=(
            "The refund exceeds the $500 base threshold and the active Enterprise Plus "
            "exception does not apply to this case."
        ),
        evidence_ids=evidence,
        confidence=1.0,
    )
