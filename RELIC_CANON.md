# ReLiC Authority & Continuity Canon

Status: governing project canon for this repository.

## ReLiC is whole

**ReLiC is ReLiC and is never only a portion of the whole.** A demonstration may exercise one duty, but it must not redefine ReLiC as that duty.

The complete ReLiC lifecycle is:

`REMEMBER -> EXIST -> LIVE -> IMAGINE -> CREATE -> SHARE -> REMEMBER`

### REMEMBER

Preserve the evidence needed for continuity: errors and corrections, canon, applicable laws and authority records, successful/known-working states, backups/reference states, provenance, decisions, and why changes occurred. Historical state remains evidence; it does not silently become current authority.

### EXIST

ReLiC exists as a continual reference boundary. Before a downstream action that depends on ReLiC authority proceeds, applicable authority, provenance, time, known errors, and current context must be resolved. Missing, failed, conflicting, or unknown required authority must not be converted into permission by model confidence or historical success.

### LIVE

Observe the current environment and preserve environmental identity through time. In system/hardware environments this includes available performance, stability, resource, fault, thermal/health, and other authorized telemetry. Historical readings remain historical; current observations establish the current environmental record. Observation does not itself grant mutation authority.

### IMAGINE

Permit hypotheses, simulations, models, and fiction to be tested without presenting them as truth. ReLiC keeps `KNOWN`, `EVIDENCE`, `INFERENCE`, `HYPOTHESIS/FICTION`, `TEST`, and `RESULT` distinguishable. A hypothesis may become supported only through evidence and verification; plausibility alone does not promote it to truth.

### CREATE

Create the traceable report/context package that allows an AI, human, or other authorized connector to follow ReLiC authority. A created representation must retain source, time, provenance, applicable authority, uncertainty/conflict, relevant errors/working references, test/verification evidence, and result. Creation is representation, not automatic truth or execution authority.

### SHARE

Expose ReLiC's inner workings and proof surface for review. For this hackathon, ReLiC Share exists so AMD can inspect what ReLiC remembered, what authority existed, what environment was observed, what was imagined/tested, what was created, what evidence supports the result, and what remains unknown. **Share is a window into ReLiC; Share is not ReLiC itself.**

“Remember. Explain. Prove.” describes the Share proof experience. It does not replace the full ReLiC lifecycle.

## Core doctrine

1. **Representation is not truth.** A rendered answer, generated explanation, model output, summary, or newest file is not automatically authoritative.
2. **Identity is not output equivalence.** Similar outputs do not establish that two records, authorities, models, or states are the same thing.
3. **Evidence, interpretation, plan, execution, and result remain distinguishable.** ReLiC preserves the links between them instead of flattening them into one answer.
4. **Corrections remain evidence.** A corrected or superseded record is retained with its history; it is not silently erased.
5. **Errors become durable lessons.** Known failures and their corrections are recorded in `ERRORS.md` and linked to decision/change history when possible.
6. **Known-working code is evidence.** Backups/reference states identify versions proven to work at a known point. A backup is not automatically current canon; it is a recovery and comparison reference.
7. **Why must survive what.** Changes record not only what changed but why, under which authority, and what evidence justified the change.
8. **Neurons organize; they do not legislate.** Neuron records organize plans, dependencies, questions, and intended work. They cannot silently create or override authority.
9. **RuneCore structures meaning; it does not invent authority.** RuneCore maps evidence, authority, intent, and relationships into stable machine-readable structures while preserving provenance.
10. **ReLiC is Environmental Intelligence and continuity infrastructure.** ReLiC may remember, retrieve, compare, trace, observe, test hypotheses, flag conflict, construct context, create reports, and share proof. It must not silently rewrite history, promote inference/fiction to truth, or acquire execution authority merely by observing an environment.

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

AI, ReLiC, RuneCore, Neurons, project canon, memorandums, and internal rules remain subordinate to **applicable human law**. Internal authority must never be interpreted as permission for an AI system to violate applicable law. When an internal instruction appears to conflict with applicable law, the system preserves the conflict as evidence and requires lawful handling, including human escalation when appropriate.

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

ReLiC is a continual reference and Environmental Intelligence layer, but reference/observation is not execution authority. RuneCore/ReLiC context can constrain, inform, block, escalate, or explain a workflow according to applicable authority while the execution substrate remains separately identified, authorized, and verified.

AMD/vLLM execution is not claimed until an AMD-backed endpoint is actually configured and verified. AMD hardware-health monitoring or processor tuning is not claimed until authorized telemetry/control interfaces are connected and verified. Evolus integration is not claimed until it is actually connected and verified.