# Human Law Source Architecture for ReLiC Share

Status: hackathon engineering design and source registry.

## Scope and truth boundary

There is no single finite database called “all human law.” Law is jurisdictional, temporal, hierarchical, amended continuously, and includes constitutions, enacted statutes, regulations, court decisions, court rules, treaties/international agreements, and local ordinances. ReLiC therefore must not claim that it has loaded or resolved all human law.

The implementable requirement is: **when a decision can be affected by human law, ReLiC must identify the relevant jurisdiction and legal source classes, retrieve from authoritative sources, preserve the source text and time/provenance, resolve applicability without inventing precedence, and escalate unresolved legal interpretation to a qualified human.**

This file records the official source families researched for the U.S./North Carolina demonstration. It is a source map, not a legal opinion and not a representation that every law in every source has been ingested.

## Federal United States source families

### Constitution

Source family: Constitution of the United States and constitutional interpretation.

Primary research source: Constitution Annotated, Congress.gov / Library of Congress: https://constitution.congress.gov/

ReLiC treatment: record constitutional provision identity separately from annotations and judicial interpretations. Do not treat explanatory annotation as the constitutional text itself.

### Enacted federal statutes — session law / slip law

Official source: U.S. Government Publishing Office, Public and Private Laws: https://www.govinfo.gov/app/collection/plaw

Official permanent session-law collection: United States Statutes at Large: https://www.govinfo.gov/app/collection/STATUTE/

GovInfo states that slip laws are official publications and that the Statutes at Large is the permanent collection of laws and resolutions enacted during each session of Congress.

ReLiC treatment: preserve Public Law number, Statutes at Large citation when available, enactment date, affected provisions, and source edition. Enacted text is historical evidence even after amendment or repeal; do not delete it.

### Codified federal statutes — United States Code

Official source: Office of the Law Revision Counsel, U.S. House of Representatives: https://uscode.house.gov/

The OLRC describes the U.S. Code as the consolidation and codification by subject matter of the general and permanent laws of the United States. The online Code is maintained from the same database used to prepare printed Code volumes. The Code site distinguishes positive-law titles from titles that are prima facie evidence.

Download/release-point source: https://uscode.house.gov/download/download.html

ReLiC treatment: retain title, section, edition/release point, positive-law status when relevant, source URL, retrieval time, effective/amendment relationships, and links back to enactments when necessary. Never assume the newest codified text applied to an older event.

### Federal regulations

Current research source: Electronic Code of Federal Regulations: https://www.ecfr.gov/

The eCFR describes the CFR as the official legal print publication of general and permanent agency rules and describes the eCFR as a continuously updated online version that is not itself the official legal edition.

Official publication / rulemaking source: Federal Register: https://www.federalregister.gov/

ReLiC treatment: distinguish proposed rule, final rule, effective rule, codified CFR text, amendment, correction, stay, delay, and withdrawal. Store agency, CFR citation, Federal Register citation, publication date, effective date, version/retrieval date, and authority citation. A proposed rule must never be promoted to current law merely because it is newer.

### Federal judicial decisions

U.S. Supreme Court official opinions: https://www.supremecourt.gov/opinions/opinions.aspx

ReLiC treatment: preserve court, case identity, docket/citation, decision date, opinion status/version, holding/context extracted for the task, and subsequent treatment when known. Separate majority/controlling judgment from concurrence, dissent, syllabus, party argument, and model-generated interpretation. ReLiC must not infer that a case controls a particular dispute solely from keyword similarity.

For lower federal courts, ReLiC should use the relevant court's official source or an official federal judiciary source when available and preserve court/circuit jurisdiction explicitly.

### Treaties and international agreements applicable to the United States

U.S. Department of State Office of Treaty Affairs source family: https://www.state.gov/

Treaties and International Acts Series / treaty-text guidance has historically been published by the Department of State. Treaties in Force identifies agreements carried on State Department records as in force as of the publication date. Treaty status is time-sensitive and source editions must be retained.

ReLiC treatment: distinguish treaty text, executive agreement, signature, ratification/consent status, entry into force, reservation/declaration/understanding, amendment, termination/supersession, and applicability. Never infer domestic enforceability merely from the existence of an international instrument.

## North Carolina source families

### North Carolina Constitution and statutes

North Carolina General Assembly laws portal: https://www.ncleg.gov/Laws

General Statutes: https://www.ncleg.gov/Laws/GeneralStatutes

Session Laws: https://www.ncleg.gov/Laws/SessionLaws

The General Assembly site states its online General Statutes include a stated currency point and also warns that the online statutes are not the official printed version. The Session Laws archive reaches back to 1777.

ReLiC treatment: preserve statute/session-law identity, chapter/section, session-law number, effective dates, amendment history when relevant, source currency/caveat, and jurisdiction. When current codification and an enacted session law differ because an update is pending, retain both and mark the conflict/currency issue for resolution rather than silently choosing one.

### North Carolina administrative rules

North Carolina Office of Administrative Hearings Rules Division: https://www.oah.nc.gov/rules-division

North Carolina Administrative Code information: https://www.oah.nc.gov/rules-division/participating-rulemaking-process/about-north-carolina-administrative-code

North Carolina Register: https://www.oah.nc.gov/rules-division/north-carolina-register

OAH states that the NCAC compiles administrative rules and is updated on its website; the North Carolina Register is published twice monthly and contains proposed rules, rulemaking notices, executive orders, and other Chapter 150B material.

ReLiC treatment: distinguish NCAC rule text from proposed rulemaking and Register notices. Preserve agency/board, NCAC citation, authority note, effective date, publication/version date, rulemaking history, and any periodic-review/expiration status that is relevant.

### North Carolina judicial decisions and court rules

North Carolina Judicial Branch appellate opinions: https://www.nccourts.gov/documents/appellate-court-opinions

North Carolina Supreme Court rules: https://www.nccourts.gov/courts/supreme-court/court-rules

The Judicial Branch publishes Supreme Court and Court of Appeals opinions and publishes rules of practice, procedure, and conduct adopted by the Supreme Court.

ReLiC treatment: keep judicial opinions and court rules as different authority classes. Preserve court, publication status, decision date, case/citation, procedural posture when relevant, and subsequent history. Do not treat an unpublished decision, dissent, summary/headnote, or lower-court decision as equivalent to a controlling published holding.

## Local law

Local ordinances and codes vary by county, municipality, special district, and subject. There is no single national source that can establish every local rule.

ReLiC treatment: jurisdiction resolution must identify the location and governmental entity relevant to the event, then retrieve the ordinance/code from that government's official publication or officially designated code publisher. Preserve ordinance number, code section, adopting authority, enactment/effective date, amendment/repeal history, territorial scope, and source status. Never assume that a rule from one municipality applies in another.

## Required ReLiC legal record model

A human-law Rune should not be merely `{text: "law"}`. The minimum engineering record should support:

```text
id
record_type
jurisdiction
jurisdiction_level
issuing_authority
source_family
source_url
source_document_id / citation
source_status
text_or_hash/reference
enacted_or_decided_at
effective_from
effective_to
published_or_recorded_at
retrieved_at
amends
corrects
supersedes
repeals
stays_or_delays
precedential_status
scope
applicability_conditions
currency_statement
verification_status
interpretation_status
human_review_required
```

Not every field applies to every authority type. Missing fields remain UNKNOWN rather than being synthesized.

## ReLiC incorporation pipeline

```text
EVENT / QUESTION
      ↓
1. IDENTIFY JURISDICTION
   federal / state / county / municipality / other
      ↓
2. IDENTIFY LEGAL SOURCE CLASSES THAT MAY APPLY
   constitution / statute / regulation / case / court rule / treaty / ordinance
      ↓
3. RETRIEVE AUTHORITATIVE SOURCE
   preserve source identity + retrieval time + source status
      ↓
4. TEMPORAL RESOLUTION
   what text/status was effective for the event date?
      ↓
5. RELATIONSHIP RESOLUTION
   amendment / correction / supersession / repeal / stay / controlling case history
      ↓
6. APPLICABILITY CHECK
   jurisdiction + subject + actor + event + exceptions + effective time
      ↓
7. CONFLICT / UNCERTAINTY CHECK
   do not convert missing or conflicting authority into permission
      ↓
8. HUMAN REVIEW WHEN LEGAL INTERPRETATION IS MATERIAL OR UNRESOLVED
      ↓
9. CREATE TRACE
   sources + authority IDs + reasoning boundary + unknowns + result
      ↓
10. REMEMBER
   retain the decision context, later corrections, and why the result changed
```

## Precedence is not a hard-coded universal list

ReLiC must not use a simplistic rule such as “federal always beats state” or “newest always wins.” Legal precedence depends on jurisdiction, subject, source type, court hierarchy, preemption, effective dates, procedural status, and other legal doctrines. ReLiC should encode relationships and source metadata, retrieve potentially applicable authority, and escalate unresolved interpretation rather than inventing a universal ordering.

## Temporal law is essential to ReLiC

For any historical event, ReLiC should be able to distinguish:

```text
LAW AS ENACTED
LAW AS CODIFIED AT TIME T
LAW AS AMENDED LATER
LAW AS INTERPRETED BY COURT AT TIME T
CURRENT LAW
WHAT ReLiC KNEW / RETRIEVED AT TIME T
```

A later amendment does not rewrite the historical source. A repeal does not mean the repealed law never existed. A later judicial decision can change the interpretation relevant to a present analysis without erasing the earlier decision. This is the same continuity principle implemented by the prototype's valid-time/recorded-time separation.

## Retention and updates

Legal records should be immutable source snapshots or content-addressed references where feasible. New versions create new records linked by amendment/correction/supersession/repeal relationships. ReLiC should periodically check source currency for authority being actively relied upon, but a refresh must not overwrite the historical version used for an earlier decision.

## What ReLiC must never claim without evidence

- that it contains all human law;
- that an online source is official when the publisher labels it unofficial;
- that a newer law applies retroactively;
- that a proposed rule is effective law;
- that a case is controlling without jurisdiction/precedent analysis;
- that a treaty is domestically enforceable merely because it exists;
- that a local ordinance applies outside its jurisdiction;
- that a model's legal interpretation is legal authority;
- that absence from a search proves no law exists;
- that ReLiC replaces qualified legal review.

## Hackathon implementation status

This document defines the researched source architecture and incorporation requirements. The current repository does **not** contain a complete legal corpus, automated ingestion from every source above, a citator, or a general legal reasoning engine. Those capabilities must remain PROPOSAL / IMPLEMENTATION WORK until code and verification evidence exist.
