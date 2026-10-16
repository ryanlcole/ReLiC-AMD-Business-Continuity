from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from app.aws_control import aws_control_chat, aws_control_evidence


@dataclass(frozen=True)
class ObservationRecord:
    observation_type: str
    status: str
    observed_at: str
    execution_provider: str
    amd_backed: bool
    verification_scope: str
    model: str
    region: str
    stop_reason: str | None
    output_sha256: str
    output_text: str
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    latency_ms: int | None
    boundary: str

    def as_dict(self) -> dict:
        return {
            "observation_type": self.observation_type,
            "status": self.status,
            "observed_at": self.observed_at,
            "execution_provider": self.execution_provider,
            "amd_backed": self.amd_backed,
            "verification_scope": self.verification_scope,
            "model": self.model,
            "region": self.region,
            "stop_reason": self.stop_reason,
            "output_sha256": self.output_sha256,
            "output_text": self.output_text,
            "usage": {
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "total_tokens": self.total_tokens,
            },
            "latency_ms": self.latency_ms,
            "boundary": self.boundary,
        }


def observe_aws_control(
    messages: list[dict[str, str]],
    *,
    executor: Callable[..., dict] = aws_control_chat,
    observed_at: str | None = None,
) -> ObservationRecord:
    """Execute the AWS control and reduce the response to ReLiC observation evidence.

    This is an observation boundary, not a canon-ingestion function. It does not
    write to the durable ReLiC event store and it never promotes AWS execution
    into AMD-backed evidence.
    """
    response = executor(messages)
    evidence = aws_control_evidence(response)
    output_text = evidence["output_text"]
    timestamp = observed_at or datetime.now(timezone.utc).isoformat()
    return ObservationRecord(
        observation_type="inference-execution",
        status="observed",
        observed_at=timestamp,
        execution_provider=evidence["execution_provider"],
        amd_backed=evidence["amd_backed"],
        verification_scope=evidence["verification_scope"],
        model=evidence["model"],
        region=evidence["region"],
        stop_reason=evidence["stop_reason"],
        output_sha256=hashlib.sha256(output_text.encode("utf-8")).hexdigest(),
        output_text=output_text,
        input_tokens=evidence["usage"]["input_tokens"],
        output_tokens=evidence["usage"]["output_tokens"],
        total_tokens=evidence["usage"]["total_tokens"],
        latency_ms=evidence["latency_ms"],
        boundary=evidence["boundary"],
    )
