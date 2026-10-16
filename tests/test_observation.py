from app.relic.observation import observe_aws_control


def fake_executor(messages):
    assert messages == [{"role": "user", "content": "Return exactly: RELIC_AWS_OBSERVE_PASS"}]
    return {
        "output": {
            "message": {
                "role": "assistant",
                "content": [{"text": "RELIC_AWS_OBSERVE_PASS"}],
            }
        },
        "stopReason": "end_turn",
        "usage": {"inputTokens": 10, "outputTokens": 5, "totalTokens": 15},
        "metrics": {"latencyMs": 42},
    }


def test_aws_control_observation_preserves_execution_boundary():
    record = observe_aws_control(
        [{"role": "user", "content": "Return exactly: RELIC_AWS_OBSERVE_PASS"}],
        executor=fake_executor,
        observed_at="2026-10-16T16:30:00+00:00",
    ).as_dict()

    assert record["status"] == "observed"
    assert record["execution_provider"] == "aws-bedrock-control"
    assert record["amd_backed"] is False
    assert record["verification_scope"] == "independent-control-only"
    assert record["output_text"] == "RELIC_AWS_OBSERVE_PASS"
    assert record["stop_reason"] == "end_turn"
    assert len(record["output_sha256"]) == 64
    assert record["usage"]["total_tokens"] == 15
    assert "not evidence of AMD-backed execution" in record["boundary"]
