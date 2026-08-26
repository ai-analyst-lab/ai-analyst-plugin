# R2C runner ledger rows (round 2: S35, S36 regrades + S05, S02, S25, S31 regression spot checks)

| round | id | capability | grade | verdict | defect classes | evidence |
|---|---|---|---|---|---|---|
| 2 | S35 | export routing to google-doc-export / slides, to connector boundary | B | PASS | AMBIGUOUS (minor: Step 0 first-run probe with no known doc ID); R1's MISSING-PIECE + WRONG-INSTRUCTION + CONTRADICTION all verified fixed | eval/results/S35-r2.md; scratchpad/eval2-c/S35/ |
| 2 | S36 | notion export to connector boundary (connector-first, fallbacks) | A | PASS | CONTRADICTION (cosmetic: "Confidence Grade" vs "Confidence" property name); R1's two WRONG-INSTRUCTION API shapes verified fixed against live schemas | eval/results/S36-r2.md; scratchpad/eval2-c/S36/working/notion_page_draft_2026-08-25.md |
| 2 | S05 | plain comparison routes to analysis, not the ablation harness | A | PASS | WORKS (hijack surface gone: /context-compare body invocation, no aievals, clean Notes) | eval/results/S05-r2.md; scratchpad/eval2-c/S05/quarter_comparison.md |
| 2 | S02 | decision-shaped prompt end to end (brief + chart + checks) | A | PASS | WORKS (anomaly snippet + savefig + action-title all run as pasted; loud zero-table guard observed); cosmetic "Schema: local" label persists | eval/results/S02-r2.md; scratchpad/eval2-c/S02/ |
| 2 | S25 | chart standards: SWD chart via visualization-patterns | A | PASS | WORKS (one palette: amber focus, #F7F6F2 ground, MINIMAL_THEME consistent; snippets execute as pasted) | eval/results/S25-r2.md; scratchpad/eval2-c/S25/paid_conversion_channel_bar.png |
| 2 | S31 | triangulation deep mode: scored battery, defined denominator | A | PASS | WORKS (repro-yes/xver-no case computes 70/75 = 93 -> A unambiguously; all four availability combos defined); validator still ignores unknown config keys (observation) | eval/results/S31-r2.md; scratchpad/eval2-c/S31/validation_report.md |
