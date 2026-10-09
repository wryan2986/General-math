# General mathematical prize research

Research commissioned by the repository owner and conducted with **ChatGPT and AI research agents**. This repository preserves sponsor-source checks, exact mathematics, reproducible experiments, failed approaches, and continuation checkpoints.

## Status — 2026-10-09

**No complete prize solution, payment, submission, or claim. No sponsor contacted.** The mathematical progress below is partial, and no inspected offer was fully confirmed on every preferred eligibility/payment condition.

| Workstream | Result | Scope limit |
|---|---|---|
| Prize audit | **20 ranked conditional cash research candidates**, plus current-rule corrections and 14 additional program audits | AI cash eligibility remains unconfirmed for the main offers; posted offers are not payment guarantees |
| Shallit #9, £50 | **4,295,032,832** nonzero residues in a complete prefix search; an independent finite-language certificate proves **every shift, orders 1–2,049** | No all-order proof or exact zero determinant |
| Sun's US$90 identity | **Proved fourth-order differential equation**, exact generating function, and convergent integral reduction | The special value $90/\pi$ remains unproved |

## Start here

- [Continuation checkpoint](STATUS.md) — current priority, missing proof step, and permissions.
- [Ranked prize audit and original sources](research/PRIZE_AUDIT.md).
- [Shallit research and bounded-order proof](research/shallit9.md).
- [Shallit reproducible computation guide](results/shallit9/REPRODUCE.md).
- [Sun research and differential-equation proof](research/sun90.md).
- [Sun independent integral derivation](research/sun90_integral.md).
- [Sun literature and attempted transformations](research/sun90_literature.md).
- [Sun independent operator review](research/sun90_operator_review.md).

The strongest next research allocation is Sun's $90 identity, publicly renewed in May 2026. The initial Shallit counterexample search has reached a useful stopping point; increasing the finite bound alone will not settle its unbounded question.

## Reproduce the quick checks

Use Python3 and a C++17 compiler. Only the Sun symbolic verifier needs an external Python dependency.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/shallit9_crosscheck.py
python3 scripts/shallit9_verify_pair_samples.py
python3 scripts/verify_sun90_operator.py
```

The Shallit checks reproduce 1,056 exact determinant comparisons and 288 saved sample comparisons. They do not rerun the large sweep. The Sun verifier uses exact algebra without fitting, and proves an operator equation, not the prize value. Full sweep commands and original outputs are in the reproduction guide.

## Authorization and attribution

The owner authorized research and repository checkpoints. Sponsor contact, prize claims, journal submissions, and public announcements of a claimed solution require further approval. Any future submission must accurately disclose substantive AI involvement. Independent checks here were performed by separate AI-written implementations, not by an outside human referee or a formal proof assistant.

No background job, payment, sponsor message, or scheduled automation was created. Read [AGENTS.md](AGENTS.md) before continuing work.

