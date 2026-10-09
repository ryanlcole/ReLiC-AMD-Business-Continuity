from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Iterable


@dataclass(frozen=True)
class RatePeriod:
    """A compensation fact with both valid-time and recorded-time provenance."""

    id: str
    person_id: str
    amount: str
    valid_from: str
    valid_to: str | None
    recorded_at: str
    source: str
    authority_id: str
    supersedes: str | None = None

    @property
    def rate(self) -> Decimal:
        return Decimal(self.amount)

    def applies_on(self, day: date) -> bool:
        start = date.fromisoformat(self.valid_from)
        end = date.fromisoformat(self.valid_to) if self.valid_to else None
        return start <= day and (end is None or day <= end)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class WorkRecord:
    id: str
    person_id: str
    worked_on: str
    units: str
    paid_amount: str
    recorded_at: str


@dataclass(frozen=True)
class Adjustment:
    work_id: str
    worked_on: str
    units: str
    rate_then_used: str
    rate_now_applicable: str
    paid_amount: str
    correct_amount: str
    delta: str
    authority_id: str


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _active_records(records: Iterable[RatePeriod]) -> list[RatePeriod]:
    by_id = {record.id: record for record in records}
    superseded = {record.supersedes for record in by_id.values() if record.supersedes}
    return [record for record in by_id.values() if record.id not in superseded]


def applicable_rate(records: Iterable[RatePeriod], person_id: str, on_date: date) -> RatePeriod:
    candidates = [
        record for record in _active_records(records)
        if record.person_id == person_id and record.applies_on(on_date)
    ]
    if not candidates:
        raise LookupError(f"No applicable rate for {person_id} on {on_date.isoformat()}")
    # Later valid_from wins; recorded_at breaks ties so corrections are deterministic.
    return max(candidates, key=lambda r: (r.valid_from, r.recorded_at, r.id))


def current_rate(records: Iterable[RatePeriod], person_id: str, today: date) -> RatePeriod:
    return applicable_rate(records, person_id, today)


def reconcile_history(
    rates: Iterable[RatePeriod], work: Iterable[WorkRecord], person_id: str
) -> list[Adjustment]:
    """Re-evaluate past work against the authority that is now known to apply then.

    This supports retroactive/backdated corrections without rewriting the original
    work/payment record. A positive delta means additional compensation is due; a
    negative delta means the historical payment exceeded the now-applicable amount.
    Any real payment action remains subject to applicable human law and approval.
    """

    adjustments: list[Adjustment] = []
    for item in work:
        if item.person_id != person_id:
            continue
        day = date.fromisoformat(item.worked_on)
        rate = applicable_rate(rates, person_id, day)
        units = Decimal(item.units)
        correct = units * rate.rate
        paid = Decimal(item.paid_amount)
        delta = correct - paid
        adjustments.append(
            Adjustment(
                work_id=item.id,
                worked_on=item.worked_on,
                units=str(units),
                rate_then_used=str(paid / units) if units else "0",
                rate_now_applicable=str(rate.rate),
                paid_amount=str(paid),
                correct_amount=str(correct),
                delta=str(delta),
                authority_id=rate.authority_id,
            )
        )
    return adjustments
