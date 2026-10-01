# dcs-conformance — one page

## What it is

A compliance engine that folds multiple sources of evidence using
Belnap FOUR-valued logic, producing signed, replayable artifacts in
OSCAL and in-toto formats.

## The problem

Every compliance tool collapses evidence to pass/fail. When two tools
disagree — a scanner says PASS, an auditor says FAIL — the tool drops
one of them. Compliance teams spend 30–40% of audit cycle reconciling
by hand.

## The differentiation

`dcs` treats disagreement as a first-class state (`CONFLICT`). Every
verdict traces to named sources with named reasons. Every bundle is
Ed25519-signed and independently verifiable by any Sigstore-aware tool.
Every result is exported as OSCAL — consumable by FedRAMP/RMF tooling
without installing anything.

## Coverage today

- 232 controls across 130+ subsystems
- 7 source connectors: GitHub, AWS, OpenSCAP, kube-bench, Kyverno,
  Prowler, model cards
- 2 formats: OSCAL 1.1.2, in-toto v1 / DSSE
- 1 signature scheme: Ed25519 (verifiable with public key only)
- Second manifest (AI governance, 15 controls) ships as of this release

## What's not there yet

- Hosted multi-tenant service (in progress — public verifier at
  verify.dcs.dev)
- SSO, RBAC, dashboard
- Connector library beyond the seven

## Pricing

- Per-requirement folded: $0.10 / MUST / month, $0.05 / SHOULD, $0.01 / MAY
- Minimum $500/mo
- Pilot: $5,000 for 90 days, includes hosted verifier and 10h of engineering

## Who this is for

- AI companies shipping to EU (EU AI Act) or US federal (FedRAMP 20x)
- 3PAOs and RMF shops reconciling scanner + manual findings
- Financial services under FFIEC or PCI 4.0 multi-source validation

## Contact

Danny — danny@dannylabs.example — github.com/Danny-TMIG/enterprise-aiops
