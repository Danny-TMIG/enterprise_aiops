# Why binary compliance fails when your scanner and your auditor disagree

Every compliance tool in the market makes the same assumption: a control
is either passing or failing. Vanta, Drata, Secureframe, Prowler, OPA,
Kyverno, OpenSCAP — each one collapses the messy reality of multiple
observers into a single bit.

That collapse is the problem.

## The moment it breaks

Consider a real sequence. Your cloud scanner reports `encryption_at_rest: PASS`
for a production S3 bucket. Your auditor, reading the same policy against
the same bucket three weeks later, records `FAIL` because the bucket was
never enabled for server-side encryption with a customer-managed key.
Both are right. The scanner checked a different property than the auditor.
The binary tool printed one of them and dropped the disagreement.

Multiply this across SOC 2, FedRAMP, HIPAA, PCI 4.0, and the EU AI Act.
Now you have five tools, six sources of truth, and no vocabulary for what
happens when two of them disagree. Compliance teams spend 30–40% of their
audit cycle manually reconciling tool outputs precisely because the tools
cannot represent disagreement.

## The fix: a lattice, not a bit

Belnap's FOUR-valued logic has been standard in paraconsistent reasoning
since 1977. It adds two states to the classical two:

| State | Meaning |
|---|---|
| T | evidence says true |
| F | evidence says false |
| U | no evidence either way |
| B | evidence says both (CONFLICT) |

When a scanner says T and an auditor says F, the fold is B. Not T. Not F.
B. The system now has a state for the disagreement, and that state is
signed, timestamped, and replayable.

## What this makes possible

A compliance engine that folds Belnap FOUR instead of collapsing to a bit
gives a compliance team three things no vendor currently offers:

1. **A conflict queue.** Every control where sources disagree becomes a
   work item with the disagreement preserved, not overwritten.
2. **A signed evidence bundle.** The verdict, every attestation, and every
   source are bundled, signed with Ed25519, and independently verifiable.
3. **An OSCAL export.** The result is machine-consumable by the entire
   NIST / FedRAMP tooling ecosystem without installing anything new.

## Why now

Three regulatory deadlines force multi-source reconciliation:

- **FedRAMP 20x** (2025) requires automated, cryptographically signed
  evidence with third-party verification.
- **EU AI Act** (Aug 2025–26) requires a risk register, technical
  documentation, human oversight, and accuracy reporting — five sources
  that will disagree in practice.
- **PCI 4.0** (2025) requires control validation from multiple independent
  points, which means multi-source fold by definition.

Every one of these is a compliance regime where binary verdicts are
insufficient. Every one of them is now in force or in transition.

## The engine is the product

`dcs-conformance` ships today on PyPI. It folds seven source families —
GitHub, AWS, OpenSCAP, kube-bench, Kyverno, Prowler, model cards — across
232 controls. It exports both OSCAL 1.1.2 Assessment Results and in-toto
v1 DSSE envelopes. Both are verifiable by tools the buyer already owns.

    pip install dcs-conformance
    dcs self

The output is a signed bundle in which every claim traces back to a named
source with a named reason. When two sources disagree, you see B. When one
source has no opinion, you see U. When they agree, you see T or F.

## The category nobody named yet

There are twenty open-source compliance tools. None of them fold. The
market they serve is not "GRC" or "CSPM" or "policy-as-code." It is the
space between them — the reconciliation layer that every auditor
eventually builds by hand.

That layer is the product.

The compliance industry has spent twenty years building tools that produce
verdicts. The next twenty are about reconciling them. The first tool that
ships this as a primitive wins the fold.
