from __future__ import annotations

"""Read-only Model Context Protocol surface for ReLiC Share.

This server exposes the hackathon repository's ReLiC continuity evidence to MCP
hosts without granting mutation or execution authority. MCP is a transport and
context interface; it does not make a record true, applicable, or authoritative.
"""

import json
from pathlib import Path
from typing import Any

from mcp.server import MCPServer

from app.relic import continuity_snapshot, evaluate_case

ROOT = Path(__file__).resolve().parents[1]
RELIC_DATA = ROOT / "data" / "relic"
DEMO_DATA = ROOT / "data" / "demo-company"

mcp = MCPServer("ReLiC Share")


def _read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _read_json(relative_path: str) -> Any:
    return json.loads(_read_text(relative_path))


@mcp.resource("relic://canon")
def canon() -> str:
    """Governing ReLiC canon for this hackathon repository."""
    return _read_text("RELIC_CANON.md")


@mcp.resource("relic://errors")
def errors() -> str:
    """Durable ReLiC Share error and correction ledger."""
    return _read_text("ERRORS.md")


@mcp.resource("relic://authority")
def authority() -> str:
    """Machine-readable ReLiC authority records."""
    return json.dumps(_read_json("data/relic/authority.json"), indent=2)


@mcp.resource("relic://human-law/sources")
def human_law_sources() -> str:
    """Registry of researched human-law source families and official source URLs."""
    return json.dumps(_read_json("data/relic/human_law_sources.json"), indent=2)


@mcp.resource("relic://human-law/architecture")
def human_law_architecture() -> str:
    """Engineering architecture for incorporating human-law records into ReLiC."""
    return _read_text("docs/HUMAN_LAW_SOURCE_ARCHITECTURE.md")


@mcp.resource("relic://changes")
def changes() -> str:
    """Material ReLiC Share change-history records."""
    return json.dumps(_read_json("data/relic/change_history.json"), indent=2)


@mcp.resource("relic://working-references")
def working_references() -> str:
    """Known-working comparison/recovery references."""
    return json.dumps(_read_json("data/relic/working_references.json"), indent=2)


@mcp.resource("relic://neurons")
def neurons() -> str:
    """ReLiC planning/dependency neurons. Neurons organize; they do not legislate."""
    return json.dumps(_read_json("data/relic/neurons.json"), indent=2)


@mcp.resource("relic://demo/policies")
def demo_policies() -> str:
    """Synthetic policy, exception, and correction evidence used by the demo."""
    return json.dumps(_read_json("data/demo-company/policies.json"), indent=2)


@mcp.tool()
def get_continuity_snapshot() -> dict:
    """Return the current repository continuity inventory produced by RuneCore."""
    return continuity_snapshot()


@mcp.tool()
def evaluate_demo_refund(
    amount: float,
    customer_tier: str,
    enterprise_plus_active: bool = False,
) -> dict:
    """Run the deterministic synthetic refund demonstration and return its evidence IDs."""
    result = evaluate_case(amount, customer_tier, enterprise_plus_active)
    return {
        "case": {
            "amount": amount,
            "customer_tier": customer_tier,
            "enterprise_plus_active": enterprise_plus_active,
        },
        "decision": result.as_dict(),
        "inference_mode": "deterministic-local-reference",
        "authority_boundary": (
            "This synthetic demonstration does not establish real-world legal applicability."
        ),
    }


@mcp.tool()
def get_human_law_source_registry() -> dict:
    """Return the researched source registry; this is not a complete corpus of human law."""
    records = _read_json("data/relic/human_law_sources.json")
    return {
        "status": "source-registry-not-complete-law-corpus",
        "records": records,
        "boundary": (
            "Source discovery does not establish jurisdiction, applicability, precedence, "
            "current validity, or legal advice."
        ),
    }


if __name__ == "__main__":
    # The official MCP CLI can run this server over stdio or Streamable HTTP.
    # Example: mcp run app/mcp_server.py --transport streamable-http
    pass
