from app.relic import evaluate_case


def test_base_policy_auto_approves_at_threshold():
    result = evaluate_case(500, "Standard", False)
    assert result.action == "auto_approve"
    assert result.evidence_ids == ["POL-2026-01"]


def test_standard_customer_over_threshold_requires_manager():
    result = evaluate_case(750, "Enterprise Standard", False)
    assert result.action == "manager_approval"
    assert "COR-2026-04" in result.evidence_ids


def test_inactive_plus_requires_manager():
    result = evaluate_case(750, "Enterprise Plus", False)
    assert result.action == "manager_approval"


def test_active_plus_uses_exception_and_correction():
    result = evaluate_case(750, "Enterprise Plus", True)
    assert result.action == "auto_approve"
    assert result.evidence_ids == ["POL-2026-01", "EXC-2026-03", "COR-2026-04"]


def test_active_plus_over_exception_limit_requires_manager():
    result = evaluate_case(1000.01, "Enterprise Plus", True)
    assert result.action == "manager_approval"
