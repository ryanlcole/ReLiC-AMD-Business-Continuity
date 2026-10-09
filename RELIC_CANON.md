# ReLiC Authority & Continuity Canon

Status: governing project canon for this repository.

## Core doctrine

1. **Representation is not truth.** A rendered answer, generated explanation, model output, summary, or newest file is not automatically authoritative.
2. **Identity is not output equivalence.** Similar outputs do not establish that two records, authorities, models, or states are the same thing.
3. **Evidence, interpretation, plan, execution, and result remain distinguishable.** ReLiC preserves the links between them instead of flattening them into one answer.
4. **Corrections remain evidence.** A corrected or superseded record is retained with its history; it is not silently erased.
5. **Errors become durable lessons.** Known failures and their corrections are recorded in `ERRORS.md` and linked to the decision/change history when possible.
6. **Known-working code is evidence.** Backups/reference states identify versions proven to work at a known point. A backup is not automatically current canon; it is a recovery and comparison reference.
7. **Why must survive what.** Changes should record not only what changed but why, under which authority, and what evidence justified the change.
8. **Neurons organize; they do not legislate.** Neuron records organize plans, dependencies, questions, and intended work. They cannot silently create or override authority.
9. **RuneCore structures meaning; it does not invent authority.** RuneCore maps evidence, authority, intent, and relationships into stable machine-readable structures while preserving provenance.
10. **ReLiC is observer/continuity infrastructure.** ReLiC may retrieve, compare, trace, flag conflict, and construct context. It must not silently rewrite history or promote an inference to authority.

## Authority records

Canon, rules, laws, and memorandums are all **authority-bearing record types**. Their titles do not by themselves determine precedence. ReLiC evaluates at least:

- issuer / source,
- jurisdiction or project scope,
- effective time,
- explicit precedence,
- amendment/correction/supersession relationships,
- applicability to the decision,
- evidence/provenance.

A memorandum may therefore change an applicable project rule when the issuing authority and scope permit it; a file named `CANON` cannot override a higher applicable authority merely because of its filename.

## Human law boundary

AI, ReLiC, RuneCore, Neurons, project canon, memorandums, and internal rules remain subordinate to **applicable human law**. Internal authority must never be interpreted as permission for an AI system to violate applicable law. When an internal instruction appears to conflict with applicable law, the system should preserve the conflict as evidence and require lawful handling, including human escalation when appropriate.

This repository does not claim that its software can independently determine all applicable law. Legal applicability can depend on jurisdiction, facts, and competent human/legal interpretation.

## Authority classes

The initial machine-readable classes are:

- `human_law`
- `canon`
- `rule`
- `memorandum`
- `decision`
- `correction`
- `error`
- `working_reference`
- `plan`

`human_law` is a boundary class, not a claim that an ingested text is legally valid merely because it is labeled that way. Provenance and validation remain required.

## Change rule

A material change should be traceable as:

`prior state -> evidence/trigger -> authority -> reason -> change -> verification -> resulting state`

When a change fails, the failure is added to `ERRORS.md`; when a prior state was known working, its commit/reference is preserved in the continuity ledger.

## Execution boundary

RuneCore/ReLiC context can guide an inference or workflow, but the execution substrate is separately identified and verified. AMD/vLLM execution is not claimed until an AMD-backed endpoint is actually configured and verified. Evolus integration is not claimed until it is actually connected and verified.
