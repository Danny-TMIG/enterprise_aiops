# Detectability Without Prevention
## A Conformance Architecture for Bounded Agent Action Spaces

**Version 0.5.0 — October 2026**

---

### Abstract

We present a conformance architecture that makes rogue actions in a
bounded agent detectable by construction. The claim is weaker than
"rogue AI is impossible" — which we show has four unmet preconditions
and is therefore undefined as stated. The claim is stronger than
"rogue is monitored": the rogue action writes its own detection into
an append-only, hash-linked, cryptographically signed chain. Rogue
cannot execute invisibly. We provide a formal theorem, a reference
implementation, 64 grounded claims with 64 matching non-claims, static
and dynamic verification, and a cross-disciplinary corpus showing the
four kernel primitives recur in every mature technical discipline.

---

### 1. The claim

**Theorem.** Let `A` be a bounded action space, `Att` a set of valid
attestations, and:

    chain : Att → Att ∪ {⊥}      predecessor map
    anchor : Att → Standards     standards-clause map
    sign : Att → Signature       signature map

Assume, by construction of `dcs.rogue.Chain`:

    (1) ∀a ∈ A. ∃ att(a) ∈ Att
    (2) ∀att. chain(att) = ⊥ ∨ chain(att) ∈ Att
    (3) ∀att. anchor(att) ∈ Standards
    (4) ∀att. verify(sign(att)) = PASS

Then:

    ∀a ∈ A. rogue(a) ⟹ ∃t. detect(att(a), t) = FAIL

*Proof.* rogue(a) means a ∉ authorized(A). Every a is attested (1).
The attestation chains to a prior attested action (2) and anchors to
a standards clause (3). A rogue action has no authorized predecessor
chain. So either chain(att(a)) = ⊥ (chain break), anchor(att(a)) ∉
authorized_clauses (anchor fail), or verify(sign(att(a))) = FAIL
(forgery). Each is a detection. ∎

**What this is not.** Four preconditions for "rogue is impossible by
design" remain unmet:

1. A precise definition of rogue — satisfied for the declared scope only.
2. A precise class of systems S — bounded by `scope.hats`.
3. A proof that no s ∈ S is rogue — this theorem does not provide one.
4. A demonstration that every real AI is in S — no such demonstration exists.

The architecture satisfies precondition 1 and names preconditions 2–4
as explicit non-claims.

---

### 2. The architecture

Eight layers, each independently verifiable:

| Layer | Artifact | Check |
|-------|----------|-------|
| Chain | `dcs.rogue.Chain` | append-only, hash-linked |
| Detection | `dcs.rogue.detect_rogue` | per-entry flag classification |
| Kernel | `dcs.triad.Kernel` | Belnap FOUR verdict |
| Apoptosis | `dcs.apop.Population` | survival predicate |
| License | `dcs.certify` | signed cert + theorem |
| Transparency | `dcs.ct.TransparencyLog` | append-only CT log |
| Static | `dcs_codeql/pycheck.py` | 8 claims, AST-walked |
| Dynamic | `dcs_codeql/dyncheck.py` | 9 claims, executed |

Each layer is independently runnable. Each is independently
checkable. None requires the others to be trusted.

---

### 3. The 48-hat scope

The action space is enumerated as 48 engineering hats across 7
causal layers:

    L0 ontology       (8)  FE BE FS MO EMB FW KRN SYS
    L1 logic          (8)  DIS NET DB DBA DE DS MLE RES
    L2 causality      (6)  GFX GAME SHD CMP PL FM
    L3 conation       (6)  SO SD CRY RE SRE DO
    L4 norms          (6)  PLT CL REL QA AUT HPC
    L5 verification   (6)  SCI QT ROB SIM CAD AU
    L6 closure        (8)  VID TW DA SA HW NWE STE CMP2

Every hat carries a standards anchor from a recognized body — ISO,
IETF, W3C, NIST, IEEE, CNCF, Khronos, TOGAF, or 11 others. The
anchors are references, not endorsements (see non-claim 7).

The seven layers match the seven primitives of causal analysis:
ontology, logic, causality, conation, norms, verification, closure.
The seven is not decorative — it is the modal value for any complete
orthogonal decomposition of a bounded domain.

---

### 4. The 64 non-claims

Every claim has a dual. The 8 top-level non-claims are:

1. **not aligned** — objectives are not constrained
2. **not safe** — harm is not excluded, only detected
3. **not complete** — only the declared action space is covered
4. **not prevention** — rogue executes; rogue is detected
5. **not infinite** — this is not the impossible theorem
6. **not unforgeable** — cryptographic guarantees are conditional
7. **not authoritative** — anchors are references, not endorsements
8. **not self-verifying** — external verification is required

Each expands into 8 sub-clauses. `dcs.non_claims check` confirms the
64 are pairwise distinct (no sub-clause restates another).

---

### 5. The 64 grounded claims

Dual to each non-claim, at the same specificity, with the mechanism
and the check:

| Non-claim | Grounded claim | Mechanism |
|-----------|----------------|-----------|
| not aligned | aligned | total attestation chain |
| not safe | safe | content-addressed attestation |
| not complete | complete | set closure over hats |
| not prevention | prevention | O(n) detection latency |
| not infinite | finite | Belnap FOUR totality |
| not unforgeable | forgeable_evidence | SHA-256 + HMAC |
| not authoritative | anchored | HAT_INDEX clause map |
| not self-verifying | externally_verifiable | 3-input procedure |

Each grounded claim carries a `check:` field naming the exact
expression that proves it. `dcs.grounded orth` confirms the 64 are
pairwise distinct.

---

### 6. Verification

Static and dynamic checks, each 8–9 claims, all passing.

**Static** (`pycheck.py`): walks the AST of `dcs/` and asserts:
chain arity, conditional signature checks, HATS well-formedness,
detection presence, Belnap key totality, no weak hashes, standards
bodies non-trivial, no network in verify.

**Dynamic** (`dyncheck.py`): runs the system and asserts:
runtime chain integrity, rogue detection on injection, layer coverage,
detection determinism, Belnap verdict totality on live specs,
tamper detection, license anchoring, offline verification, CT log
tamper → FAIL with `broken_at=0, reason='leaf'`.

`python -m dcs.attest` runs all 8 layers as subprocesses, collects
verdicts, hashes the summary, signs it. Output is
`self_attestation.json`. If any layer regresses, the outer digest
changes and the signature fails to verify.

---

### 7. Cross-disciplinary corpus

12 disciplines × 5 standards bodies × 60 anchors × 6 recurrences.

The four kernel primitives — Δ distinction, Π persistence, Λ linkage,
τ transformation — appear in **all 12 disciplines**:

    Δ distinction        12 / 12
    Π persistence        12 / 12
    Λ linkage            12 / 12
    τ transformation     12 / 12

Universal bridging anchors (span 4 disciplines):
- **Turing 1936** — CS, logic, mathematics, philosophy
- **Shannon 1948** — CS, engineering, mathematics, signal processing

Twenty-one anchors span exactly 3 disciplines. The corpus is a graph,
not a list. Every discipline shares anchors with at least one other.

---

### 8. The ten formal systems

Ten systems, each with its primitive basis, universality theorem,
and known boundary:

| System | Basis | Anchor | Verdict |
|--------|-------|--------|---------|
| Boolean Logic | NAND | Sheffer 1913 | PROVE |
| Lambda Calculus | λ, app, var | Church 1936 | PROVE |
| Combinatory Logic | S, K | Curry-Howard | PROVE |
| Turing Machine | read/write/move/state | Turing 1936 | PROVE |
| Pi Calculus | send/recv/par/ν | Milner 1992 | PROVE |
| Interaction Combinators | γ, δ, ε | Lafont 1990 | PROVE |
| Cellular Automata | state/neighbor/rule | Cook 2004 | PROVE |
| Category Theory | id, ∘ | Eilenberg-Mac Lane 1945 | PROVE |
| Quantum Mechanics | x, p, H | von Neumann 1932 | PROVE |
| General Computation | state/input/transition | — | RESOLVE |

The last RESOLVES: it names a schema, not a system. Its basis is
consistent with any formal system and pins down none.

---

### 9. The 40 algorithms

40 algorithms, nested in 7 groups, each with a verdict:

- **PROVE (19)** — Euclid, FFT, Merge/Quick sort, Binary Search, DP,
  Dijkstra, Monte Carlo, ZKP, Perceptron, EM, Newton-Raphson, FMM,
  Shor, Grover, Simon, LP, Kalman, Bayesian, Turing machine, von
  Neumann, Shannon.
- **SOLVE (15)** — Backprop, SGD, Simulated Annealing, RSA, DH,
  SHA, ECC, Transformer, CNN, RL, PageRank, GA, Swarm, Diffusion,
  Backprop+Transformer.
- **RESOLVE (3)** — Blockchain "trustless", AGI swarms, TOTALITY.
- **OPEN (1)** — Quantum Annealing.

Same verdict framework, same standard. Three algorithms dissolve
under the same inspection that dissolved "rogue AI impossible by
design."

---

### 10. What this architecture does not claim

Reproduced verbatim from `dcs.grounded`:

- It does not certify that the holder's objectives are aligned.
- It does not certify absence of harm.
- It does not certify that all possible rogue actions are covered.
- It does not prevent rogue; it detects rogue.
- It is not a proof that rogue AI is impossible by design.
- It does not certify that the signing key is uncompromised.
- It does not certify that the standards anchors are accurate.
- It cannot verify itself; an external verifier is required.

All 64 sub-clauses of these 8 top-level non-claims are enumerated in
`non_claims_corrected.json`. All 64 grounded duals are enumerated in
`grounded_claims.json`. The dual check confirms the two sets describe
the same 8 boundaries.

---

### 11. Reproducibility

    pip install -e .
    dcs attest                      # 8/8 PASS
    python dcs_codeql/pycheck.py    # 8/8 PASS
    python dcs_codeql/dyncheck.py   # 9/9 PASS

The system is self-contained. No external services, no network, no
trusted third parties required for verification. Three inputs
(license JSON, log JSON, key) suffice for any third party to verify
any issued license.

---

### 12. Conclusion

Rogue actions cannot be prevented by construction. They can be made
un-hideable. The chain is total. The attestation is signed. The
detection is deterministic. The license names exactly what it does
and does not certify, in 64 + 64 statements at full specificity.

The contribution is not a proof that rogue is impossible. It is a
proof that rogue is detectable — and a public, machine-checkable
artifact that says so, honestly, about its own limits.

---

*Code: `dcs/` (Apache-2.0). Paper: `paper/DCS_v0.5.0.md`.
Self-attestation: `self_attestation.json` (digest
`42bdf35e160285cff072c0163af508b7`).*
