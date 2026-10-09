from __future__ import annotations

import os
from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class AMDConfig:
    base_url: str
    api_key: str
    model: str


def get_amd_config() -> AMDConfig | None:
    base_url = os.getenv("AMD_VLLM_BASE_URL", "").strip().rstrip("/")
    api_key = os.getenv("AMD_VLLM_API_KEY", "").strip()
    model = os.getenv("AMD_VLLM_MODEL", "").strip()
    if not (base_url and api_key and model):
        return None
    return AMDConfig(base_url, api_key, model)


def amd_configured() -> bool:
    return get_amd_config() is not None


def amd_chat(messages: list[dict[str, str]], timeout: float = 30.0) -> dict:
    """Call the event AMD-hosted OpenAI-compatible vLLM endpoint.

    This function does not prove that an endpoint is AMD-backed. Verification of
    event infrastructure is a separate deployment/evidence step.
    """
    config = get_amd_config()
    if config is None:
        raise RuntimeError("AMD vLLM endpoint is not configured")
    response = httpx.post(
        f"{config.base_url}/chat/completions",
        headers={"Authorization": f"Bearer {config.api_key}"},
        json={"model": config.model, "messages": messages, "temperature": 0},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()
