---
id: ADR-000
title: README | ADR
type: adr
status: accepted
version: v1.0
canonical: true
scope: carol-anne
audience:
  - developer
  - maintainer
created: "2026-10-30"
updated: "2026-10-30"
tags:
  - governance
  - adr
provenance:
  - human
  - Claude Sonnet 5.5
---

# Architecture Decision Records (ADR)

## Purpose

This directory records the architectural decisions that shape Carol aNNe. Each record states a decision, the constraints that motivated it and its consequences, so that any later change can be traced to its origin and weighed against the reasoning that produced the current design.

## When an ADR is required

An ADR is written and accepted before work starts on a change that affects the model architecture, the input or output contract, the deployment targets, the training and evaluation protocol, data handling, or the runtime and toolchain. Work that only implements an accepted decision, such as filling in a configuration or adding a test, does not need one.

## Lifecycle

| Status | Meaning |
|--------|---------|
| `reserved` | Number allocated for a planned ADR; no content yet |
| `draft` | Under review; not in force |
| `accepted` | In force and governing current behaviour |
| `amended` | In force, with one or more decisions revised; see the amendment record |
| `superseded` | Replaced in full by a later ADR; no longer governing |

## Rules of change

- An accepted ADR is not edited silently. A change raises the version, adds an entry to the amendment record and is explained in the body.
- A decision that is replaced in full is superseded by a new ADR. The old record is marked `superseded` and points to its successor.
- This index is authoritative. It lists every ADR with its current status and is updated in the same change as the ADR itself.

## Structure of an ADR

Records are copied from `TEMPLATE.md` and keep the following section order.

| Section | Content |
|---------|---------|
| Status | Current lifecycle status |
| 1. Context | The constraints and forces behind the decision: decision drivers and rationale |
| 2. Decision | Numbered clauses (§1, §2, …), each stating one decision |
| 3. Consequences | Positive and negative effects, implementation notes and related records |
| 4. Non-goals | What the decision deliberately does not cover |
| 5. Options considered | Alternatives and the reasons they were not chosen. Optional: included when the choice was non-obvious or contested |
| Amendment record | Version, date and summary of each change. Always the last section |

Files are named `ADR-NNN-kebab-case-title.md`, where NNN is a three-digit number that is assigned in sequence and never reused. Version strings do not appear in filenames.

## Writing conventions

- **Register.** Impersonal and technical. State what the system does and why, without first or second person and without promotional language.
- **Precision.** Prefer exact figures and names, such as layer shapes, parameter counts and sampling rates, to adjectives.
- **Evidence.** Mark each value as measured, calculated or targeted, and give the conditions for a measurement.
- **Terms.** Define a term where it first appears and use it consistently afterwards.
- **Separation.** A decision clause states the decision. Its justification belongs in the context section.

## Index

- **ADR-001: Baseline Architecture**
  Path: `ADR/ADR-001-baseline-architecture.md`
  Status: accepted

## Amendment record

| Version | Date | Summary |
|---------|------|---------|
| v1.0 | 2026-10-30 | Accepted |
| v0.2 | 2026-10-30 | Restructured as a statement of scope, lifecycle, rules and writing conventions; ADR-001 indexed |
| v0.1 | 2026-10-30 | Initial index and rules; no ADRs yet |
