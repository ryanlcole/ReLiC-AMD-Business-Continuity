from app.relic.runecore import (
    continuity_snapshot,
    load_authority_runes,
    load_change_history,
    load_neurons,
    load_working_references,
)


def test_authority_ledger_has_project_canon_and_human_law_boundary():
    runes = load_authority_runes()
    by_id = {rune.id: rune for rune in runes}
    assert by_id["AUTH-RELIC-CANON-001"].record_type == "canon"
    assert by_id["AUTH-HUMAN-LAW-BOUNDARY-001"].record_type == "human_law"


def test_continuity_records_preserve_why_and_working_state():
    changes = load_change_history()
    assert changes
    assert all(record.get("why") for record in changes)
    references = load_working_references()
    assert references[0]["git_commit"] == "43d5fc2fa4bfda0b5770e8fef382d751c0a21679"


def test_neurons_are_plan_records_not_authority_substitutes():
    neurons = load_neurons()
    assert neurons
    assert all(neuron["kind"] == "plan" for neuron in neurons)


def test_snapshot_exposes_human_law_boundary():
    snapshot = continuity_snapshot()
    assert snapshot["human_law_boundary_present"] is True
    assert snapshot["working_references"] >= 1
    assert snapshot["neurons"] >= 1
