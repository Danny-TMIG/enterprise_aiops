# Five openings. Pick one. Delete the rest.

## Opening 1 — The one I wrote

Every compliance tool in the market makes the same assumption: a
control is either passing or failing. Vanta, Drata, Secureframe,
Prowler, OPA, Kyverno, OpenSCAP — each one collapses the messy
reality of multiple observers into a single bit.

That collapse is the problem.

## Opening 2 — The concrete story

Your cloud scanner reports `encryption_at_rest: PASS` for a
production S3 bucket. Your auditor, reading the same policy against
the same bucket three weeks later, records `FAIL`. Both are right.
The scanner checked a different property than the auditor.

Your tool printed one of them and dropped the disagreement. That is
what every compliance tool does. It is also why your audit cycle
takes three months instead of three weeks.

## Opening 3 — The regulatory clock

Three regulatory deadlines are forcing multi-source reconciliation
in the next eighteen months. FedRAMP 20x requires cryptographically
signed automated evidence. The EU AI Act requires a risk register,
technical documentation, human oversight, and accuracy reporting —
five sources that will disagree in practice. PCI 4.0 requires
control validation from multiple independent points.

Every one of these is a compliance regime where binary verdicts are
insufficient. And every one of them is now in force.

## Opening 4 — The mathematical provocation

In 1977, Nuel Belnap formalized a four-valued logic that includes
both `UNKNOWN` and `CONFLICT` as first-class states. For forty-eight
years, it has been applied to circuit design, genomics, and
databases. It has never been applied to compliance.

That is the gap. This is the tool.

## Opening 5 — The blunt one

Compliance tools lie.

Not intentionally. But every one of them collapses multiple sources
of truth into a single pass/fail, and in doing so they drop the
disagreement that your CISO actually needs to see. When the scanner
says yes and the auditor says no, your tool prints whichever it saw
first and moves on.

The fix is forty-eight years old. Belnap FOUR. Four states instead
of two. Disagreement preserved, not overwritten.

---

## Which one?

- **Opening 1** if your audience is technical and patient. It earns trust.
- **Opening 2** if your audience is operational and skeptical. It names their day.
- **Opening 3** if your audience is a regulator or compliance lead. It names the deadline.
- **Opening 4** if your audience is HN. It names the gap and the fix in one breath.
- **Opening 5** if your audience is a CISO or a CFO. It earns attention fast.

Pick one. Delete the rest. The rest of the essay is already written
in `essay.md`.
