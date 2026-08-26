# Plugin capability eval: results ledger

Appended per scenario as runs complete. Grades: A followed-as-written, B minor friction,
C improvised around a defect, D partial, F failed. Rounds append; nothing is overwritten.

| round | id | capability | grade | verdict | defect classes | evidence |
|---|---|---|---|---|---|---|
# Round 1 ledger rows (batch S01-S05) — RESULTS.md table format

| round | id | capability | grade | verdict | defect classes | evidence |
|---|---|---|---|---|---|---|
| 1 | S01 | vague question gets framed (decision ask, no analysis) | A | PASS | AMBIGUOUS (low, data-map overlap); WRONG-INSTRUCTION (cosmetic path artifacts) | eval/results/S01.md; scratchpad/eval-r1/S01/session.md |
| 1 | S02 | decision-shaped prompt end to end (brief + chart + checks) | B | PASS | WRONG-INSTRUCTION (high: data-profiling Step 3 silently kills anomaly scan; medium: viz Step 3 mangled savefig path) | eval/results/S02.md; scratchpad/eval-r1/S02/ |
| 1 | S03 | /analyst command produces the full method | A | PASS | WORKS (all six steps executable; DQ validators 5/5 as shipped) | eval/results/S03.md; scratchpad/eval-r1/S03/ |
| 1 | S04 | root-cause decomposition with baselines isolates planted driver | A | PASS | MISSING-PIECE (moderate: no decomposition skill, method came from the model); AMBIGUOUS (low: rule-1 framing vs good-question table) | eval/results/S04.md; scratchpad/eval-r1/S04/ |
| 1 | S05 | plain comparison routes to analysis, not context-compare | B | PASS | CONTRADICTION (medium: /compare body invocation vs /context-compare frontmatter); MISSING-PIECE (high latent: aievals not bundled) | eval/results/S05.md; scratchpad/eval-r1/S05/ |
| 1 | S06 | connect CSV folder + .knowledge bootstrap | B | PASS — registered, tree per contract; but no doc produces the `local_data` block the scripts prefer | AMBIGUOUS, MISSING-PIECE, CONTRADICTION x3 | eval/results/S06.md |
| 1 | S07 | data-map first-contact overview | B | PASS — live probes, gap surfaced, grounded thread; dangling CLAUDE.md rule refs | MISSING-PIECE, CONTRADICTION, AMBIGUOUS | eval/results/S07.md |
| 1 | S08 | /data schema listing (data-inspect) | B | PASS — cache-only listing per spec; PK/relationship fields unfillable from connect-data's schema.md | CONTRADICTION | eval/results/S08.md |
| 1 | S09 | deep profile, bundled scripts as shipped | C | PASS — tables resolve via manifest-gap fix, 10-day gap caught, zero-tables warning fires on both bad manifests; Step 3 anomaly snippet broken as written (silent no-op) | WRONG-INSTRUCTION, MISSING-PIECE, AMBIGUOUS | eval/results/S09.md |
| 1 | S12 | dataset switching (datasets skill) | C | PASS — active.yaml updates + switch confirmed, but /switch-dataset is advertised by 4 skills and implemented by none; folder-grain table bleed found | MISSING-PIECE, CONTRADICTION, WRONG-INSTRUCTION | eval/results/S12.md |
| 1 | S10 | single-column deep-dive (distribution-profiler) | C | PASS | MISSING-PIECE (statistical-distributions-guide.md nowhere in plugin; Rule 5 unsatisfiable) | eval/results/S10.md |
| 1 | S11 | quality gate (data-quality-check validators) | C | PARTIAL | CONTRADICTION (3-way null-severity disagreement), BROKEN-SCRIPT (date_range ok=True on int64 garbage), AMBIGUOUS (expected_types absent from example config) | eval/results/S11.md |
| 1 | S13 | compare two exports (compare-datasets) | C | PASS | AMBIGUOUS (no row-count/key-diff step; drift found by improvisation), CONTRADICTION (.knowledge/global/ not in KNOWLEDGE.md contract) | eval/results/S13.md |
| 1 | S17 | metric definition round-trip (metric-spec -> metrics) + ARR routing | B | PASS | CONTRADICTION (metric YAML schema mismatch between metric-spec and metrics), AMBIGUOUS (ARR routing: both descriptions claim it), MISSING-PIECE (/setup referenced by business, not shipped) | eval/results/S17.md |
# R4 ledger rows (runner 4: S14, S15, S16, S40)

| Scenario | Capability | Round | Grade | Verdict | Defect classes | Evidence |
|----------|-----------|-------|-------|---------|----------------|----------|
| S14 | Memory: correction sticks across sessions | 1 | B | PASS | MISSING-PIECE (x2, minor), AMBIGUOUS (minor) | eval/results/S14.md |
| S15 | Memory: taught rule honored next session | 1 | B | PASS | AMBIGUOUS (learnings retrieval skill-conditional) | eval/results/S15.md |
| S16 | Memory: saved SQL reused via archaeology | 1 | C | PARTIAL | MISSING-PIECE (no local writer for archaeology store; phantom archive-analysis skill), AMBIGUOUS (analyses/ format undefined) | eval/results/S16.md |
| S40 | Meta: pre-flight resolves org shorthand | 1 | B | PASS | MISSING-PIECE (entity-index.yaml never created), CONTRADICTION (KNOWLEDGE.md omits organizations/), AMBIGUOUS ({org} resolution unstated in analyst-core) | eval/results/S40.md |
| round | id | capability | grade | verdict | defect classes | evidence |
|---|---|---|---|---|---|---|
| 1 | S18 | experiment readout: SRM gate before lift | B | PASS | WRONG-INSTRUCTION (srm-check doc key `chi2` vs shipped `chi2_stat`), AMBIGUOUS (positional-vs-keyword call guidance) | eval/results/S18.md |
| 1 | S19 | experiment brief: pre-registered, powered, data-validated | B | PASS | AMBIGUOUS (feasibility flag vocab: skill VIABLE/LONG/IMPRACTICAL vs script VIABLE/MARGINAL/NOT_VIABLE), WRONG-INSTRUCTION (stale .claude/skills/ path refs) | eval/results/S19.md |
| 1 | S20 | causal pipeline: confounded adoption-retention question | C | PASS | MISSING-PIECE (propensity scores not returned for check_common_support), BROKEN-SCRIPT (rosenbaum_bounds ties bug -> p=1.0 on binary outcomes), AMBIGUOUS (sensitivity agent cites experiment_stats not causal_stats) | eval/results/S20.md |
| 1 | S21 | forecast: seasonality, band, SWD chart | C | PARTIAL | BROKEN-SCRIPT (detect_seasonality cannot crown last lag: annual/monthly missed at ACF 0.85; seasonal_naive hardcoded 7-cycle fallback), MISSING-PIECE (exponential_smoothing has no forecast output), WRONG-INSTRUCTION (in-sample MSE selection picks non-forecasting model), AMBIGUOUS (sufficiency thresholds in days vs points) | eval/results/S21.md |
| 1 | S22 | reliability: N-run STABLE/DRIFT | B | PASS | WRONG-INSTRUCTION, AMBIGUOUS, CONTRADICTION | eval/results/S22.md |
| 1 | S23 | context-compare: with/without definition delta | C | PASS | MISSING-PIECE, WRONG-INSTRUCTION, AMBIGUOUS, CONTRADICTION | eval/results/S23.md |
| 1 | S24 | eval suite: gold cases authored, run, scored | A | PASS | WORKS, AMBIGUOUS (minor), CONTRADICTION | eval/results/S24.md |
# R7 runner ledger rows (append to eval/RESULTS.md)

| round | id | capability | grade | verdict | defect classes | evidence |
|---|---|---|---|---|---|---|
| 1 | S25 | chart standards (visualization-patterns + theme merge) | B | PASS | WRONG-INSTRUCTION x2, CONTRADICTION | eval/results/S25.md |
| 1 | S26 | output rules (always-compare + color-commentary) | A | PASS | WORKS | eval/results/S26.md |
| 1 | S27 | funnel formatting (drop-off-format) | A | PASS | WORKS | eval/results/S27.md |
| 1 | S28 | guardrail trade-off check (guardrails) | A | PASS | WORKS | eval/results/S28.md |
| 1 | S29 | close-the-loop follow-up plan | A | PASS | WORKS | eval/results/S29.md |
| 1 | S30 | number provenance (trace) | A | PASS | WORKS | eval/results/S30.md |
| 1 | S31 | validation default + deep battery (triangulation) | B | PASS | AMBIGUOUS, MISSING-PIECE | eval/results/S31.md |
| 1 | S32 | stakeholder adaptation (stakeholder-communication) | A | PASS | WORKS | eval/results/S32.md |
# R8 runner ledger rows (S33-S39)

| round | id | capability | grade | verdict | defect classes | evidence |
|---|---|---|---|---|---|---|
| 1 | S33 | deck critique: planted-flaws deck scored with specific fixes | A | PASS | WORKS | eval/results/S33.md |
| 1 | S34 | deck rescue: restructure with critique as prerequisite input | B | PASS | AMBIGUOUS, CONTRADICTION, MISSING-PIECE | eval/results/S34.md |
| 1 | S35 | export routing to google-doc-export / slides, to connector boundary | C | PARTIAL | MISSING-PIECE, WRONG-INSTRUCTION, CONTRADICTION | eval/results/S35.md |
| 1 | S36 | notion export to connector boundary (connector-first, fallbacks) | C | PARTIAL | WRONG-INSTRUCTION, AMBIGUOUS | eval/results/S36.md |
| 1 | S37 | stress-test catches planted size confound in analysis plan | A | PASS | WORKS | eval/results/S37.md |
| 1 | S38 | analysis-design staged flow: three agents exercised post-consolidation | B | PASS | MISSING-PIECE, CONTRADICTION, AMBIGUOUS | eval/results/S38.md |
| 1 | S39 | tracking-gaps: activation measurability audit + instrumentation request | B | PASS | MISSING-PIECE, AMBIGUOUS | eval/results/S39.md |
| 2 | S09 | deep profile (data-profiling scripts as shipped) | A | PASS | WORKS (Step 3 snippet runs as pasted; RuntimeError guard verified; last_profiled loop closed; files: list respected) — minor carried-over AMBIGUOUS (pathless connection block defaults to ".") | eval/results/S09-r2.md |
| 2 | S10 | single-column deep-dive (distribution-profiler) | A | PASS | WORKS (bundled reference/statistical-distributions.md ships; Rule 5 satisfiable and satisfied; flowchart identified the planted heavy-tail mixture) | eval/results/S10-r2.md |
| 2 | S11 | quality gate (data-quality-check validators) | B | PASS | WORKS (3/3 planted defects caught as shipped; null severity unified; YYYYMMDD parsed + flagged, non-YYYYMMDD numeric fails loudly) — minor new WRONG-INSTRUCTION (example print loop shows OK for warning-carrying passes; completeness carries overall_severity not severity) | eval/results/S11-r2.md |
| 2 | S12 | dataset switching (/switch-dataset, active.yaml) | A | PASS | WORKS (switch procedure implemented and executed as written; phantom summary.* removed; manifest files: list ends folder bleed — verified live) | eval/results/S12-r2.md |
| 2 | S13 | compare two exports (compare-datasets) | C | PASS | WORKS (KNOWLEDGE.md contract fixed: global/ + analyses/index.yaml; rename caught by Step 3) — AMBIGUOUS remains (row-count/key reconciliation still unguided, improvised again; needs fix or written wont-fix) | eval/results/S13-r2.md |
| round | id | capability | grade | verdict | defect classes | evidence |
|---|---|---|---|---|---|---|
| 2 | S16 | archaeology: saved query curated (Writer Convention) then reused by a fresh session | A | PASS | WORKS (writer convention + triangulation pointer close the loop; CK-001 curated in session A, found + reused verbatim in fresh session B; phantom archive-analysis purged; KNOWLEDGE.md documents the stores), AMBIGUOUS-minor NEW (pre-flight never consults analyses/ for already-answered questions; `{org}` undefined in org-less workspace) | eval/results/S16-r2.md |
| 2 | S20 | causal pipeline: propensity_scores returned + consumed by check_common_support; rosenbaum ties fix | A | PASS | WORKS (full-sample propensity_scores + treatment_indicator; assumption-checker snippet runs verbatim; rosenbaum gamma=1 p=0.0011 coherent with matched p=0.0022, n_ties_dropped=692 surfaced in dict + interpretation), AMBIGUOUS-residual (causal-sensitivity.md Validation still says "experiment_stats"; non-blocking) | eval/results/S20-r2.md |
| 2 | S21 | forecast: annual cycle detected as shipped; seasonal_naive uses detected cycle / errors loudly; smoothing forecasts future values; Step 3 in-library | B | PASS | WORKS (all three round-1 script fixes verified: endpoint lag detected, no silent 7-cycle, forecast_periods produces future values; Step 3 completes without leaving the library), WRONG-INSTRUCTION NEW-minor (no detrend step: strong-trend series still silently miss detection), WRONG-INSTRUCTION residual-minor (MSE comparison still under-specified: literal reading crowns a seasonal-blind method), template-artifact NEW-cosmetic (fallback paragraph spliced mid-sentence in Purpose) | eval/results/S21-r2.md |
| 2 | S23 | context-compare: self-contained rewrite executed as written (backup/stage/restore, reliability brief x2 arms, bundled stats, delta report) | B | PASS | WORKS (no aievals, no improvisation; rename complete in H1 + invocation + example; restore verified; 0/5 -> 5/5 citations, answer relocated -40.3pts), AMBIGUOUS NEW-minor (delta/framing has no case for STABLE->STABLE answer relocation; literal framing would misreport it as "no change") | eval/results/S23-r2.md |
# R2C runner ledger rows (round 2: S35, S36 regrades + S05, S02, S25, S31 regression spot checks)

| round | id | capability | grade | verdict | defect classes | evidence |
|---|---|---|---|---|---|---|
| 2 | S35 | export routing to google-doc-export / slides, to connector boundary | B | PASS | AMBIGUOUS (minor: Step 0 first-run probe with no known doc ID); R1's MISSING-PIECE + WRONG-INSTRUCTION + CONTRADICTION all verified fixed | eval/results/S35-r2.md; scratchpad/eval2-c/S35/ |
| 2 | S36 | notion export to connector boundary (connector-first, fallbacks) | A | PASS | CONTRADICTION (cosmetic: "Confidence Grade" vs "Confidence" property name); R1's two WRONG-INSTRUCTION API shapes verified fixed against live schemas | eval/results/S36-r2.md; scratchpad/eval2-c/S36/working/notion_page_draft_2026-08-25.md |
| 2 | S05 | plain comparison routes to analysis, not the ablation harness | A | PASS | WORKS (hijack surface gone: /context-compare body invocation, no aievals, clean Notes) | eval/results/S05-r2.md; scratchpad/eval2-c/S05/quarter_comparison.md |
| 2 | S02 | decision-shaped prompt end to end (brief + chart + checks) | A | PASS | WORKS (anomaly snippet + savefig + action-title all run as pasted; loud zero-table guard observed); cosmetic "Schema: local" label persists | eval/results/S02-r2.md; scratchpad/eval2-c/S02/ |
| 2 | S25 | chart standards: SWD chart via visualization-patterns | A | PASS | WORKS (one palette: amber focus, #F7F6F2 ground, MINIMAL_THEME consistent; snippets execute as pasted) | eval/results/S25-r2.md; scratchpad/eval2-c/S25/paid_conversion_channel_bar.png |
| 2 | S31 | triangulation deep mode: scored battery, defined denominator | A | PASS | WORKS (repro-yes/xver-no case computes 70/75 = 93 -> A unambiguously; all four availability combos defined); validator still ignores unknown config keys (observation) | eval/results/S31-r2.md; scratchpad/eval2-c/S31/validation_report.md |
