---
id: ADR-000
title: README | ADR
type: adr
status: draft
version: v0.1
canonical: pending
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

This directory (`ADR/`) holds the architecture and governance decisions for Carol aNNe.

ADRs capture why a decision was made, so that a sub-optimal decision can always be traced to its origin and its reasoning. No structural change is implemented without a corresponding accepted ADR.

## Rules

1. **ADR before implementation.** An ADR is written and accepted before anything structural is built, installed, configured or chosen.
2. **No silent edits.** Once an ADR is `accepted`, its decisions are not quietly reworded. A change increments the version, adds an Amendment record entry and is explained in the body.
3. **Supersession needs a new ADR.** When an accepted ADR is fully replaced, a new ADR is written, the old one is marked `superseded`, and it points to its successor.
4. **This index is authoritative.** It lists every ADR and its current status, and is updated whenever an ADR is added or changes status.
5. **Frontmatter on every document.** Field order and formatting follow `TEMPLATE.md`.

## Status vocabulary

| Status | Meaning |
|--------|---------|
| `reserved` | Number allocated for a planned ADR; no content yet |
| `draft` | Being written; not yet in force |
| `accepted` | Adopted and currently governing behaviour |
| `amended` | Governing current behaviour; one or more decisions revised, see the Amendment record |
| `superseded` | Replaced entirely by a later ADR; no longer governing |

## File naming

`ADR/ADR-NNN-kebab-case-title.md`, where NNN is a three-digit, zero-padded, incrementing number that is never reused. Version strings never appear in filenames. New ADRs are started from `ADR/TEMPLATE.md`; the section order there is fixed.

## Index

No ADRs have been written yet. The next number is **ADR-001**.

## Amendment record

| Version | Date | Summary |
|---------|------|---------|
| v0.1 | 2026-10-30 | Initial index and rules; no ADRs yet |
