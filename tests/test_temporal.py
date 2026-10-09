from datetime import date

from app.relic.temporal import RatePeriod, WorkRecord, applicable_rate, current_rate, reconcile_history


def rates():
    return [
        RatePeriod("r1", "worker-1", "20.00", "2026-01-01", "2026-03-31", "2026-01-01T12:00:00+00:00", "memo-a", "auth-a"),
        RatePeriod("r2", "worker-1", "25.00", "2026-04-01", None, "2026-04-01T12:00:00+00:00", "memo-b", "auth-b"),
    ]


def test_rate_depends_on_when_work_occurred():
    assert applicable_rate(rates(), "worker-1", date(2026, 2, 1)).amount == "20.00"
    assert current_rate(rates(), "worker-1", date(2026, 10, 9)).amount == "25.00"


def test_backdated_correction_reconciles_without_rewriting_work():
    corrected = rates() + [
        RatePeriod("r3", "worker-1", "22.00", "2026-02-01", "2026-02-28", "2026-10-09T20:08:00+00:00", "correction-c", "auth-c")
    ]
    work = [WorkRecord("w1", "worker-1", "2026-02-10", "8", "160.00", "2026-02-10T22:00:00+00:00")]
    result = reconcile_history(corrected, work, "worker-1")[0]
    assert result.paid_amount == "160.00"
    assert result.correct_amount == "176.00"
    assert result.delta == "16.00"
    assert result.authority_id == "auth-c"


def test_superseded_record_is_not_current_authority():
    original = RatePeriod("old", "worker-1", "20", "2026-01-01", None, "2026-01-01T00:00:00+00:00", "old", "a-old")
    correction = RatePeriod("new", "worker-1", "21", "2026-01-01", None, "2026-02-01T00:00:00+00:00", "new", "a-new", supersedes="old")
    assert applicable_rate([original, correction], "worker-1", date(2026, 1, 15)).id == "new"
