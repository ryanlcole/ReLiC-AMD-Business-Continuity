from app.aws_control import aws_control_chat, aws_control_evidence, get_aws_control_config


class FakeBedrock:
    def __init__(self):
        self.call = None

    def converse(self, **kwargs):
        self.call = kwargs
        return {
            "output": {
                "message": {
                    "role": "assistant",
                    "content": [{"text": "RELIC_AWS_CONTROL_PASS"}],
                }
            },
            "stopReason": "end_turn",
            "usage": {"inputTokens": 21, "outputTokens": 7, "totalTokens": 28},
            "metrics": {"latencyMs": 189},
        }


def test_control_defaults_are_explicitly_aws(monkeypatch):
    monkeypatch.delenv("AWS_CONTROL_REGION", raising=False)
    monkeypatch.delenv("AWS_CONTROL_MODEL", raising=False)
    config = get_aws_control_config()
    assert config.region == "us-east-1"
    assert config.model == "openai.gpt-oss-20b-1:0"


def test_control_call_uses_credential_chain_and_fixed_temperature():
    fake = FakeBedrock()
    response = aws_control_chat(
        [{"role": "user", "content": "Return exactly: RELIC_AWS_CONTROL_PASS"}],
        client=fake,
    )
    assert response["stopReason"] == "end_turn"
    assert fake.call["inferenceConfig"]["temperature"] == 0
    assert fake.call["messages"][0]["content"][0]["text"].endswith("RELIC_AWS_CONTROL_PASS")


def test_control_evidence_cannot_claim_amd():
    fake = FakeBedrock()
    evidence = aws_control_evidence(fake.converse())
    assert evidence["execution_provider"] == "aws-bedrock-control"
    assert evidence["amd_backed"] is False
    assert evidence["verification_scope"] == "independent-control-only"
    assert evidence["output_text"] == "RELIC_AWS_CONTROL_PASS"
    assert "not evidence of AMD-backed execution" in evidence["boundary"]
