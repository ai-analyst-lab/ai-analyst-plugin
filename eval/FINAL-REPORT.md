# Plugin capability eval: final report (2026-08-25/26, two rounds, autonomous loop closed)

## What ran
40 scenarios covering every capability the plugin claims (EVAL-DESIGN.md), each executed as a
simulated Cowork session on synthetic data with the bundled Python run for real. Round 1: all 40
via 8 runners. Fix round: 3 tracks (bundled-code bugs with repro tests, skill-text integrity,
two flow rewrites) plus follow-up fixes. Round 2: 15 re-runs (every C, plus fix-touched
regression checks). Full evidence: eval/results/ (per-scenario reports, both rounds), FIX-ROUND-1.md.

## Grade distribution, latest grade per scenario

Round 1: 12 A / 17 B / 11 C / 0 D / 0 F
Final:   22 A / 17 B / 1 C  / 0 D / 0 F

Every round-1 C was cured or improved except compare-datasets (S13), whose missing
export-reconciliation step was fixed AFTER its regrade; the fix is applied and lint-clean but
not re-executed, so its C stands on the ledger honestly. The four fix-touched regression checks
(S02, S05, S25, S31) all ROSE from B to A: the fix round introduced zero regressions.

## What the eval proved works (highlights)
- The core method: vague asks get framed, decision-shaped asks produce brief + chart + checks,
  planted drivers isolated exactly, parts reconciling to the dollar.
- The corrections memory loop closes across sessions for real, and now the archaeology
  query-reuse loop does too (curated SQL found and reused verbatim by a fresh session).
- The discipline layer: SRM gate blocks before any lift read; guardrail check catches a
  degraded "win"; causal pipeline kills a confounded +18.2pp naive read down to the planted
  truth; the reliability/definition story reproduces (drift collapses when a definition lands).
- The gold-suite eval runs cold from its own documentation (round-1 A).
- Statistical bug fixes verified under execution: annual-cycle detection, real future-value
  forecasts, Rosenbaum ties, propensity scores to common support, loud date-dtype failures,
  one canonical null-severity table.

## Known imperfections shipped (all minor, with reasons)
- S13 re-verification pending (fix applied post-regrade; next eval round should confirm).
- Forecast method-selection (MSE rule) still needs judgment against holdout choice; detrend
  guidance added but ACF-on-strong-trend remains a care point.
- export's first-ever-run auth probe needs a document to probe; minor ambiguity.
- profile_source labels schemas "local"; run_structural_checks ignores unknown config keys;
  a few cosmetic naming drifts. All logged in the round-2 reports.

## State of the artifact
47 skills + 13 agents + /analyst command, 117 files, lint clean (path/secret/residue checks),
installed and verified via the local marketplace. Snapshot of the pre-audit tree retained at
ai-analyst-plus-preaudit/ (gitignored). The full paper trail for Shane's review: AUDIT-DESIGN.md,
FIX-DESIGN.md, EVAL-DESIGN.md, eval/FIX-ROUND-1.md, eval/RESULTS.md, eval/results/*.
