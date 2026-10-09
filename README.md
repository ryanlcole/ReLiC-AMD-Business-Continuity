# ReLiC AMD Business Continuity

**Hackathon MVP — AMD Developer Hackathon: ACT III**

ReLiC is an experimental business-continuity layer for AI agents. Instead of treating the latest retrieved text as truth, it reconstructs a traceable chain of policies, exceptions, corrections, and superseding decisions before an AI model acts.

## Problem

Business AI can retrieve a policy while missing the later correction that changes how the policy applies. That can produce confident but historically inconsistent decisions.

## MVP

This repository demonstrates a narrow, measurable case: refund-policy decisions whose rules change over time.

1. Business records are loaded as dated evidence.
2. ReLiC resolves which records remain applicable to the case.
3. The resulting evidence chain is sent to an open model through an OpenAI-compatible endpoint.
4. The model must return a decision with evidence identifiers.
5. Low-confidence or contradictory cases can be handed to a human/workflow layer.

## AMD role

The hackathon target is an open model served with **vLLM on AMD Developer Cloud / AMD GPU infrastructure**. The AMD-hosted model performs the inference shown in the final product. Local deterministic mode exists only so the application and tests can be developed before event GPU credentials are available.

## Evolus role

The planned partner integration uses Evolus for business workflow execution and human escalation. Event credentials are never committed to this repository.

## Status labels

- **IMPLEMENTED** — code exists and can be tested from this repository.
- **EXPERIMENTAL** — hypothesis or prototype; not represented as proven.
- **PLANNED** — requires event infrastructure or remains to be implemented.

Current status:

- IMPLEMENTED: deterministic provenance/continuity resolver and demo API.
- IMPLEMENTED: synthetic demo company policy/case corpus.
- PLANNED: AMD Developer Cloud vLLM endpoint verification.
- PLANNED: Evolus event-workspace integration.
- EXPERIMENTAL: Wavecore representation experiments; not required for the MVP.

## Demo scenario

- January: refunds over $500 require manager approval.
- March: Enterprise Plus customers may receive refunds up to $1,000 without manager approval.
- April: correction clarifies that the exception applies only while Enterprise Plus is active.

A $750 refund for Enterprise Standard should therefore require manager approval. The same refund for an active Enterprise Plus customer should be eligible for automatic approval.

## Sustainable preview hosting

The repository now includes a **zero-runtime-cost static reference demo** in `docs/` for GitHub Pages.

This is intentional ReLiC separation:

- **Static reference demo** — deterministic browser-side decision logic; safe to publish without secrets.
- **FastAPI service** — development/API boundary for tests and later server-side integration.
- **AMD/vLLM inference** — remains separate until real AMD infrastructure is connected and verified.
- **Evolus workflow** — remains separate until the event workspace is connected and verified.

The public preview should be hosted from the `main` branch's `/docs` folder with GitHub Pages. No API keys belong in the static site.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open `/docs` on the local server and POST a case to `/decision`.

Run tests:

```bash
pytest -q
```

## AMD / vLLM configuration

Copy `.env.example` to `.env` and set the event-provided values when available. Never commit `.env`.

The integration expects an OpenAI-compatible vLLM endpoint and can therefore be wired to the AMD-hosted model without changing ReLiC's provenance resolver.

## Repository principles

ReLiC separates evidence from inference. A source record, an interpretation of that record, and the model's final answer are different objects. Corrections are retained rather than silently replacing history, so the decision can explain not only what rule applied but how the current rule emerged.

## License

MIT. See `LICENSE`.
