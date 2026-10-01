# Cold outreach — AI governance leads

Target: Head of AI Safety, Head of Compliance, VP Engineering at Series A–C
AI companies shipping to EU or US federal customers.

---

**Subject:** when your model card and your eval report disagree

Hi {first},

Quick question. When your model card says the model handles X and your
eval report shows it fails on X, what's the current process? Spreadsheet
with two columns? Slack thread? Auditor note?

I built something that treats that disagreement as a first-class state
instead of picking a winner. You give it your model card, your eval JSON,
and a policy list from the EU AI Act or NIST AI RMF. It folds them into
one signed artifact per control, and where sources disagree you get a
CONFLICT row, not a guess.

    pip install dcs-conformance
    dcs self --manifest ai-governance

Runs locally. No SaaS. Output is OSCAL and signed in-toto envelopes
that your auditor can verify without installing anything from me.

I'm looking for three companies to run a 90-day pilot at $5k. In exchange:
early access to the hosted verifier, priority connectors, and 10 hours of
my time on your specific AI governance controls.

Worth 20 minutes to see if this maps to what you're already doing?

— Danny

---

**Follow-up (day 4):**

Hi {first} — one concrete example in case it helps. The EU AI Act
requires both a risk register (Art. 9) and accuracy reporting (Art. 15).
If your risk register lists "hallucination on medical queries" as
mitigated and your eval report shows 12% hallucination on a medical
benchmark, no current tool has a state for that. `dcs` gives you one:
`B` — conflict. The artifact tells the auditor exactly which two sources
disagree, with a hash of each.

**Follow-up (day 9):**

Hi {first} — closing the loop. If AI governance reconciliation isn't a
priority right now, no worries at all. If it becomes one, the package is
`dcs-conformance` on PyPI and the verifier is public at
`verify.dcs.dev`. Happy to pick it up whenever the timing is right.
