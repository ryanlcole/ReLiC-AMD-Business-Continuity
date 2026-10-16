from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import boto3


@dataclass(frozen=True)
class AWSControlConfig:
    region: str
    model: str


def get_aws_control_config() -> AWSControlConfig:
    """Return the independent AWS control configuration.

    AWS is a comparison/control execution substrate only. A successful AWS call
    must never be represented as AMD-backed execution evidence.
    """
    return AWSControlConfig(
        region=os.getenv("AWS_CONTROL_REGION", "us-east-1").strip() or "us-east-1",
        model=os.getenv("AWS_CONTROL_MODEL", "openai.gpt-oss-20b-1:0").strip()
        or "openai.gpt-oss-20b-1:0",
    )


def aws_control_chat(
    messages: list[dict[str, str]],
    *,
    max_tokens: int = 128,
    client: Any | None = None,
) -> dict:
    """Invoke Amazon Bedrock as an explicitly non-AMD control.

    Credentials are resolved through the normal AWS credential chain. They are
    never accepted as function arguments, returned, or written into evidence.
    """
    config = get_aws_control_config()
    runtime = client or boto3.client("bedrock-runtime", region_name=config.region)
    response = runtime.converse(
        modelId=config.model,
        messages=[
            {
                "role": message["role"],
                "content": [{"text": message["content"]}],
            }
            for message in messages
        ],
        inferenceConfig={"maxTokens": max_tokens, "temperature": 0},
    )
    return response


def aws_control_evidence(response: dict) -> dict:
    """Reduce a Bedrock response to non-secret comparison evidence."""
    output = response.get("output", {}).get("message", {})
    text = "".join(
        item.get("text", "")
        for item in output.get("content", [])
        if isinstance(item, dict)
    )
    usage = response.get("usage", {})
    metrics = response.get("metrics", {})
    config = get_aws_control_config()
    return {
        "execution_provider": "aws-bedrock-control",
        "amd_backed": False,
        "verification_scope": "independent-control-only",
        "region": config.region,
        "model": config.model,
        "stop_reason": response.get("stopReason"),
        "output_text": text,
        "usage": {
            "input_tokens": usage.get("inputTokens"),
            "output_tokens": usage.get("outputTokens"),
            "total_tokens": usage.get("totalTokens"),
        },
        "latency_ms": metrics.get("latencyMs"),
        "boundary": "AWS control success is not evidence of AMD-backed execution.",
    }
