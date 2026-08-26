# Round 1 ledger rows (batch S01-S05) — RESULTS.md table format

| round | id | capability | grade | verdict | defect classes | evidence |
|---|---|---|---|---|---|---|
| 1 | S01 | vague question gets framed (decision ask, no analysis) | A | PASS | AMBIGUOUS (low, data-map overlap); WRONG-INSTRUCTION (cosmetic path artifacts) | eval/results/S01.md; scratchpad/eval-r1/S01/session.md |
| 1 | S02 | decision-shaped prompt end to end (brief + chart + checks) | B | PASS | WRONG-INSTRUCTION (high: data-profiling Step 3 silently kills anomaly scan; medium: viz Step 3 mangled savefig path) | eval/results/S02.md; scratchpad/eval-r1/S02/ |
| 1 | S03 | /analyst command produces the full method | A | PASS | WORKS (all six steps executable; DQ validators 5/5 as shipped) | eval/results/S03.md; scratchpad/eval-r1/S03/ |
| 1 | S04 | root-cause decomposition with baselines isolates planted driver | A | PASS | MISSING-PIECE (moderate: no decomposition skill, method came from the model); AMBIGUOUS (low: rule-1 framing vs good-question table) | eval/results/S04.md; scratchpad/eval-r1/S04/ |
| 1 | S05 | plain comparison routes to analysis, not context-compare | B | PASS | CONTRADICTION (medium: /compare body invocation vs /context-compare frontmatter); MISSING-PIECE (high latent: aievals not bundled) | eval/results/S05.md; scratchpad/eval-r1/S05/ |
