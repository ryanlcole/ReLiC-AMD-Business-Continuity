import pytest

from app.amd_demo import MODEL_STATUS, _parse_json_object, build_explanation_messages, validate_explanation


DECISION = {
    "action": "auto_approve",
    "evidence_ids": ["POL-2026-01", "EXC-2026-03", "COR-2026-04"],
}


def test_prompt_contains_only_bounded_case_and_decision():
    case = {
        "amount": 750.0,
        "customer_tier": "Enterprise Plus",
        "enterprise_plus_active": True,
    }
    messages = build_explanation_messages(case, DECISION)
    assert len(messages) == 2
    assert MODEL_STATUS in messages[0]["content"]
    assert "auto_approve" in messages[1]["content"]
    assert "COR-2026-04" in messages[1]["content"]


def test_valid_model_output_is_accepted():
    payload = {
        "status": MODEL_STATUS,
        "action": "auto_approve",
        "evidence_ids": ["POL-2026-01", "EXC-2026-03", "COR-2026-04"],
        "explanation": "The deterministic policy chain permits this refund.",
    }
    explanation, action, evidence_ids = validate_explanation(payload, DECISION)
    assert explanation
    assert action == "auto_approve"
    assert evidence_ids == DECISION["evidence_ids"]


def test_model_cannot_change_action():
    payload = {
        "status": MODEL_STATUS,
        "action": "manager_approval",
        "evidence_ids": DECISION["evidence_ids"],
        "explanation": "Changed action.",
    }
    with pytest.raises(ValueError, match="changed the deterministic action"):
        validate_explanation(payload, DECISION)


def test_model_cannot_invent_or_drop_evidence():
    payload = {
        "status": MODEL_STATUS,
        "action": "auto_approve",
        "evidence_ids": ["POL-2026-01", "FAKE-999"],
        "explanation": "Invented evidence.",
    }
    with pytest.raises(ValueError, match="changed the deterministic evidence"):
        validate_explanation(payload, DECISION)


def test_json_fence_is_tolerated_without_relaxing_validation():
    parsed = _parse_json_object(
        """```json
{"status":"MODEL_INTERPRETATION_NOT_CANON","action":"auto_approve","evidence_ids":["POL-2026-01","EXC-2026-03","COR-2026-04"],"explanation":"Bounded explanation."}
```"""
    )
    assert parsed["status"] == MODEL_STATUS
