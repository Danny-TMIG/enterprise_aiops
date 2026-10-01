# Pilot Letter of Intent — dcs

**Between:** Danny-TMIG (the "Provider") and [COMPANY] (the "Customer")
**Effective date:** [DATE]
**Term:** 90 days from signature

## 1. Purpose

The Provider will deploy `dcs-conformance`, an open-source compliance
engine that folds evidence from multiple sources using four-valued
logic, in the Customer's environment as a paid pilot.

## 2. Scope

**In scope:**

- Deployment of the dcs CLI and hosted verifier into the Customer's
  CI/CD or audit pipeline
- Configuration of up to five source connectors matching the
  Customer's existing tooling (e.g., GitHub, AWS, Prowler, OpenSCAP,
  Kyverno, kube-bench, model cards, eval reports)
- Authoring or adapting a conformance manifest aligned to a
  mutually agreed framework (e.g., EU AI Act, NIST AI RMF, SOC 2,
  FedRAMP 20x)
- Ten hours of Provider engineering time over the 90-day term
- Weekly 30-minute status call

**Out of scope:**

- Custom development beyond connector configuration
- Multi-tenant SaaS deployment
- On-call support
- Any obligation to close a production contract at term end

## 3. Fees

Fixed fee: **USD $5,000**, invoiced 50% on signature, 50% on
delivery of the pilot report.

## 4. Deliverables

By day 90, the Provider will deliver:

1. A signed conformance bundle in the Customer's environment
2. An OSCAL 1.1.2 Assessment Results export of that bundle
3. An in-toto v1 DSSE envelope verifiable at `verify.dcs.dev` or
   against an exported public key
4. A written pilot report with per-control fold results, conflict
   inventory, and recommended next steps

## 5. Data handling

- All dcs execution occurs locally or in the Customer's environment.
- The Provider has no access to Customer data except what the
  Customer chooses to share for pilot reporting.
- No data leaves the Customer's environment except signed bundles
  that the Customer explicitly exports.

## 6. Confidentiality

Each party will treat the other's non-public information as
confidential for a period of two years from the effective date.

## 7. Intellectual property

- dcs-conformance is Apache-2.0 licensed. The Customer retains all
  rights to its own manifests, evidence, and configurations.
- Any new connectors authored by the Provider for this pilot remain
  Apache-2.0 and upstreamed to the public repository.

## 8. Termination

Either party may terminate for convenience with 14 days' written
notice. Fees are non-refundable once incurred.

## 9. Follow-on

At term end, the Customer may elect to convert to a production
subscription at a rate to be agreed. Terms are not binding until a
separate agreement is signed.

## 10. Signatures

**Provider:** _____________________  Date: _______
Danny-TMIG

**Customer:** _____________________  Date: _______
[NAME], [TITLE], [COMPANY]

---

*This is a letter of intent, not a binding services agreement. It
establishes scope and good faith. A separate MSA will be executed
before any work begins if either party requires one.*
