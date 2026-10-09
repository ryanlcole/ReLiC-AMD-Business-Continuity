from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Literal
import json

ROOT = Path(__file__).resolve().parents[2]
AUTHORITY_PATH = ROOT / "data" / "relic" / "authority.json"
CHANGE_HISTORY_PATH = ROOT / "data" / "relic" / "change_history.json"
WORKING_REFERENCES_PATH = ROOT / "data" / "relic" / "working_references.json"
NEURONS_PATH = ROOT / "data" / "relic" / "neurons.json"

AuthorityType = Literal[
    "human_law",
    "canon",
    "rule",
    "memorandum",
    "decision",
    "correction",
    "error",
    "working_reference",
    "plan",
]


@dataclass(frozen=True)
class AuthorityRune:
    """RuneCore representation of an authority-bearing record.

    A rune represents a sourced record. Constructing one does not prove that the
    source is valid law/canon or that it applies to a particular real-world case.
    """

    id: str
    record_type: AuthorityType
    title: str
    source: str
    issuer: str
    scope: str
    effective_date: str
    status: str

    def as_dict(self) -> dict:
        return asdict(self)

    @property
    def effective(self) -> date:
        return date.fromisoformat(self.effective_date)


def _load_json(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_authority_runes() -> list[AuthorityRune]:
    runes: list[AuthorityRune] = []
    for record in _load_json(AUTHORITY_PATH):
        runes.append(
            AuthorityRune(
                id=record["id"],
                record_type=record["record_type"],
                title=record["title"],
                source=record["source"],
                issuer=record["issuer"],
                scope=record["scope"],
                effective_date=record["effective_date"],
                status=record["status"],
            )
        )
    return runes


def load_change_history() -> list[dict]:
    return _load_json(CHANGE_HISTORY_PATH)


def load_working_references() -> list[dict]:
    return _load_json(WORKING_REFERENCES_PATH)


def load_neurons() -> list[dict]:
    return _load_json(NEURONS_PATH)


def continuity_snapshot() -> dict:
    """Return the current structured ReLiC continuity inventory.

    This is an inventory, not a claim that every authority is applicable to a
    real-world decision. Applicability and legal interpretation remain separate.
    """

    authorities = load_authority_runes()
    return {
        "authority_ids": [rune.id for rune in authorities],
        "authority_types": sorted({rune.record_type for rune in authorities}),
        "changes": len(load_change_history()),
        "working_references": len(load_working_references()),
        "neurons": len(load_neurons()),
        "human_law_boundary_present": any(
            rune.record_type == "human_law" for rune in authorities
        ),
    }
