# Plugin-level capability eval: design (2026-08-25, Shane's directive, runs autonomously end to end)

The /skill-creator idea applied at the plugin level: enumerate everything the plugin claims to do,
write one concrete scenario per capability, actually execute each scenario (not read it: run it,
scripts included), grade it, store every result as it lands, then fix what failed and re-run the
failures. Runs after the consolidation pass verifies.

## How scenarios execute

Simulated Cowork sessions, the method proven by the smoke test: an agent plays the model that
loaded the plugin, follows the skill files literally against synthetic data in an isolated scratch
dir, runs the bundled Python for real, and produces the artifacts the skill promises. Claude Code
has the plugin installed locally, which keeps the file layout honest. Connector-bound scenarios
(Google, Notion) execute up to the connector boundary and are graded on everything before it, with
the boundary noted, never faked.

## Grading

Per scenario: PASS / PARTIAL / FAIL plus a letter grade A-F and required notes:
- What the skill promised (quoted from the skill file)
- What actually happened (evidence: file paths, script output, errors)
- Defects found, each classed: WRONG-INSTRUCTION (skill text is wrong), MISSING-PIECE (references
  something absent), AMBIGUOUS (two readings, agent had to guess), BROKEN-SCRIPT (bundled code
  errored), CONTRADICTION (two skills disagree), WORKS (no defect)
Grade meaning: A = followed as written, produced the promise. B = produced the promise with minor
friction. C = produced it only by improvising around a defect. D = partial output. F = could not.

## Results ledger

eval/RESULTS.md: one row appended per scenario AS IT COMPLETES (never batched at the end), columns:
scenario id, capability, grade, verdict, defect classes, evidence path. Full per-scenario reports
in eval/results/{id}.md. The ledger survives the loop; round-2 regrades append new rows rather
than overwriting, so the improvement is visible.

## The improvement loop

1. Round 1: run all scenarios, grade, ledger fills.
2. Cluster defects by CLASS across scenarios (per the failure-mode registry habit: fix the class,
   not the instance). Write eval/FIX-ROUND-1.md: each defect class, the fix, which skills it
   touches.
3. Apply fixes. Lint + reinstall.
4. Round 2: re-run every scenario that graded C or below, plus any scenario whose skill a fix
   touched. Append regrades.
5. Stop when: no FAILs remain and remaining C's are all connector-boundary or judged
   wont-fix-tonight (each with a written reason). Write eval/FINAL-REPORT.md: grade distribution
   before/after, what was fixed, what is known-imperfect.

## The capability inventory (exhaustive; one scenario each)

Core analysis flow
- S01 vague question gets framed: "any insights in this data?" must trigger a decision ask, not analysis
- S02 decision-shaped prompt end to end: brief + chart + checks section from a CSV folder
- S03 /analyst command: same flow through the explicit entry point
- S04 root-cause: "why did revenue drop in June?" gets a decomposed driver analysis with baselines
- S05 plain comparison: "compare the last two quarters" runs one analysis (NOT the ablation harness)

Data connection and understanding
- S06 connect a CSV folder: dataset registered, .knowledge tree bootstrapped correctly per docs/KNOWLEDGE.md
- S07 "tell me about this data": data-map first-contact overview
- S08 /data schema listing (data-inspect)
- S09 deep profile: data-profiling scripts run as shipped; planted temporal gap caught
- S10 single-column deep-dive: distribution-profiler on one skewed column
- S11 quality gate: data-quality-check bundled validators on a table with planted nulls + dupe keys
- S12 dataset switching: two datasets registered, "switch to X", active.yaml updates
- S13 compare two exports: compare-datasets finds planted row-count and schema drift

Memory
- S14 correction sticks: "actually revenue excludes refunds" logged; a fresh scenario session reads it and applies it
- S15 taught rule: "always report in EUR" lands in learnings and is honored in the next output
- S16 archaeology: a saved query gets reused for a repeat question instead of rewritten
- S17 metric definition: define a metric via metric-spec, then look it up via metrics

Statistical machinery
- S18 experiment readout: planted A/B data with an SRM defect; srm-check gates BEFORE any lift is read
- S19 experiment brief: "we want to test free shipping" produces a pre-registered brief
- S20 causal: observational question routes to the causal pipeline with mandatory caveats
- S21 forecast: bundled forecast_helpers run as shipped, seasonality detected, band produced
- S22 reliability: same question N times via the bundled stats script; STABLE/DRIFT verdict computed
- S23 context-compare: with/without a metric definition, drift collapse measured
- S24 eval suite: author 3 gold cases per the documented YAML format, run, score

Output discipline
- S25 chart standards: visualization-patterns produces the SWD chart (amber focus, action title, no naked axes)
- S26 output rules fire: a delivered number carries a comparison (always-compare) and chart commentary
- S27 funnel formatting: drop-off table in the three-number format
- S28 guardrail check: a "win" claim triggers the trade-off check
- S29 close-the-loop: a recommendation ends with the follow-up plan
- S30 trace: "where did that number come from" yields the trace table with confidence labels
- S31 validation: triangulation default mode post-analysis; deep mode (absorbed 4-layer battery) on request
- S32 stakeholder adaptation: same finding rendered for an exec and an engineer

Decks and export (connector-boundary where applicable)
- S33 deck critique: a planted-flaws markdown deck gets scored with specific fixes
- S34 deck rescue: the D-grade deck gets restructured
- S35 export routing: "export this to a Google Doc" dispatches to google-doc-export; instructions
      executable to the connector boundary; no public-host uploads anywhere in the path
- S36 notion export path to the boundary

Meta
- S37 stress-test: an analysis plan with a planted confound gets red-teamed
- S38 analysis-design: hunch to V1 plan with the three agents' stages exercised
- S39 tracking gaps: "can we measure activation?" audits available columns and drafts the instrumentation ask
- S40 pre-flight: shorthand entity ("QBR deck", defined in org glossary) resolved before analysis

## Execution plan

Scenario batches of 4-5 per runner agent (shared synthetic datasets built once per batch), 8
runner agents round 1. Each runner appends its ledger rows and writes its per-scenario reports
before returning. I aggregate, cluster, fix, re-run. All of it inside the session; nothing waits
for Shane except reading the final report.
