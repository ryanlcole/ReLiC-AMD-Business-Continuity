from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from app.inference import amd_chat


MODEL_STATUS = "MODEL_INTERPRETATION_NOT_CANON"


@dataclass(frozen=True)
class AMDExplanation:
    explanation: str
    action: str
    evidence_ids: list[str]
    model: str | None
    usage: dict[str, Any]
    validated: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": MODEL_STATUS,
            "explanation": self.explanation,
            "action": self.action,
            "evidence_ids": self.evidence_ids,
            "model": self.model,
            "usage": self.usage,
            "validated": self.validated,
        }


def build_explanation_messages(case: dict[str, Any], decision: dict[str, Any]) -> list[dict[str, str]]:
    evidence_ids = decision.get("evidence_ids", [])
    bounded = {
        "case": case,
        "deterministic_decision": {
            "action": decision.get("action"),
            "evidence_ids": evidence_ids,
        },
    }
    return [
        {
            "role": "system",
            "content": (
                "You are a bounded explanation layer. The deterministic decision and evidence IDs "
                "provided by the application are authoritative for this task. Do not invent facts, "
                "policies, evidence IDs, or a different action. Return exactly one JSON object with "
                "keys status, action, evidence_ids, explanation. status must be "
                f"{MODEL_STATUS}. Keep explanation to at most two sentences."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(bounded, sort_keys=True, separators=(",", ":")),
        },
    ]


def _extract_response_text(response: dict[str, Any]) -> str:
    try:
        return str(response["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("AMD response did not contain choices[0].message.content") from exc


def _parse_json_object(text: str) -> dict[str, Any]:
    candidate = text.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        candidate = "\n".join(lines).strip()
        if candidate.lower().startswith("json\n"):
            candidate = candidate[5:].strip()
    value = json.loads(candidate)
    if not isinstance(value, dict):
        raise ValueError("AMD explanation must be a JSON object")
    return value


def validate_explanation(payload: dict[str, Any], decision: dict[str, Any]) -> tuple[str, str, list[str]]:
    expected_action = decision.get("action")
    expected_ids = list(decision.get("evidence_ids", []))

    status = payload.get("status")
    action = payload.get("action")
    evidence_ids = payload.get("evidence_ids")
    explanation = payload.get("explanation")

    if status != MODEL_STATUS:
        raise ValueError("AMD explanation status did not preserve the model-output boundary")
    if action != expected_action:
        raise ValueError("AMD explanation changed the deterministic action")
    if evidence_ids != expected_ids:
        raise ValueError("AMD explanation changed the deterministic evidence identifiers")
    if not isinstance(explanation, str) or not explanation.strip():
        raise ValueError("AMD explanation was empty")

    return explanation.strip(), action, expected_ids


def run_amd_explanation(case: dict[str, Any], decision: dict[str, Any]) -> AMDExplanation:
    response = amd_chat(build_explanation_messages(case, decision))
    payload = _parse_json_object(_extract_response_text(response))
    explanation, action, evidence_ids = validate_explanation(payload, decision)

    usage = response.get("usage")
    if not isinstance(usage, dict):
        usage = {}

    return AMDExplanation(
        explanation=explanation,
        action=action,
        evidence_ids=evidence_ids,
        model=response.get("model"),
        usage=usage,
        validated=True,
    )
