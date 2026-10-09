from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Iterable


@dataclass(frozen=True)
class RatePeriod:
    """A compensation fact with both valid-time and recorded-time provenance.

    valid_from/valid_to = when the fact applies in the world.
    recorded_at = when ReLiC Share learned the fact.
    These clocks must never be collapsed: a fact can be learned today but apply
    to work performed months ago.
    """

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

    @property
    def learned_at(self) -> datetime:
        return datetime.fromisoformat(self.recorded_at.replace("Z", "+00:00"))

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


def _known_records(records: Iterable[RatePeriod], known_at: datetime | None) -> list[RatePeriod]:
    records = list(records)
    if known_at is None:
        return records
    return [record for record in records if record.learned_at <= known_at]


def _active_records(records: Iterable[RatePeriod], known_at: datetime | None = None) -> list[RatePeriod]:
    known = _known_records(records, known_at)
    by_id = {record.id: record for record in known}
    superseded = {record.supersedes for record in by_id.values() if record.supersedes}
    return [record for record in by_id.values() if record.id not in superseded]


def applicable_rate(
    records: Iterable[RatePeriod],
    person_id: str,
    on_date: date,
    *,
    known_at: datetime | None = None,
) -> RatePeriod:
    """Resolve what rate applies to work date, optionally as knowledge existed then."""
    candidates = [
        record for record in _active_records(records, known_at)
        if record.person_id == person_id and record.applies_on(on_date)
    ]
    if not candidates:
        raise LookupError(f"No applicable rate for {person_id} on {on_date.isoformat()}")
    return max(candidates, key=lambda r: (r.valid_from, r.recorded_at, r.id))


def current_rate(records: Iterable[RatePeriod], person_id: str, today: date) -> RatePeriod:
    return applicable_rate(records, person_id, today)


def reconcile_history(
    rates: Iterable[RatePeriod], work: Iterable[WorkRecord], person_id: str
) -> list[Adjustment]:
    """Re-evaluate past work against authority now known to apply to that past.

    Original work/payment records are not rewritten. A positive delta means
    additional compensation is due mathematically; a negative delta means the
    historical payment exceeded the now-applicable amount. Actual payment or
    recovery remains subject to applicable law, contract, authority and review.
    """
    rates = list(rates)
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
