---
name: causal
description: >-
  Causal inference toolkit for when experiments are not possible: estimate treatment effects from
  observational data with assumption checks and mandatory caveats. Invoke as /causal. Trigger on
  "causal", "caused", "impact of", "effect of", "attribution", "counterfactual",
  "difference-in-differences", "DiD", "propensity matching", "pre-post". If randomization IS
  possible, route to /experiment design instead.
---
**If the skill install path cannot be resolved** (some sandboxed environments): read the script file(s) from this skill, write a copy into a `scripts/` folder inside the working folder, and run from there. The scripts are self-contained.


# Skill: /causal — OpenCausalInf Causal Inference Toolkit

## Purpose
Multi-mode skill for causal inference when experiments aren't possible. Helps users estimate treatment effects from observational data with explicit assumption checking, sensitivity analysis, and mandatory caveats. Uses the coded estimator library bundled in this skill at `scripts/causal_stats/`.

**Using the bundled library:** add this skill's `scripts/` directory to `sys.path`, then import, e.g.

```python
import sys
sys.path.insert(0, "<path to this skill>/scripts")  # the scripts/ dir next to this SKILL.md
from causal_stats import did_basic
```

Requires pandas, numpy, scipy, `statsmodels`, and `scikit-learn` (for propensity matching); install the last two in the sandbox if missing.

## When to Use
Invoke as `/causal [mode]` or trigger on causal inference intents:
- "Did this feature actually cause the improvement?"
- "We can't run an experiment, but..."
- "Was this change responsible for the metric movement?"
- "Can we measure the impact retroactively?"

## Modes

### `/causal select`
**Purpose:** Walk the method selection decision tree and recommend a causal method.
**Agent:** the `causal-method-selector` plugin agent
**Flow:**
1. Ask 4-6 diagnostic questions:
   - Can you randomize? → Route to `/experiment design`
   - Do you have a comparison group?
   - Do you have pre-treatment data?
   - Are there observable confounders you can measure?
   - How many time periods do you have?
2. Recommend: Pre-Post, DiD, PSM, Regression Adjustment, or "not feasible"
3. Output: recommended method + confidence level + rationale
**Checkpoint:** Method confirmation (Type C — user must confirm before analysis)

### `/causal analyze`
**Purpose:** Run the selected causal method on data.
**Agent:** the `causal-analyzer` plugin agent
**Flow:**
1. Read selected method from previous step or user input
2. Dispatch to the appropriate bundled estimator:
   ```python
   from causal_stats import (
       pre_post_analysis, did_basic, propensity_match,
       regression_adjust,
   )
   # Method routing:
   # "pre_post" → pre_post_analysis(pre, post, covariates)
   # "did"      → did_basic(df, outcome, treat, post)
   # "psm"      → propensity_match(df, treat, covariates, outcome)
   # "regression" → regression_adjust(df, outcome, treatment, covariates)
   ```
3. Generate charts (treatment effect, balance plots for PSM, event study for DiD)
4. Output: `working/causal_analysis_results.json`

### `/causal check`
**Purpose:** Run assumption checks for the selected method.
**Agent:** the `causal-assumption-checker` plugin agent
**Flow:**
1. Identify which assumptions apply to the selected method:
   - **DiD:** Parallel trends, no anticipation, stable composition
   - **PSM:** Common support, balance (SMD < 0.1), positivity
   - **Pre-Post:** No concurrent events, trend stability
   - **Regression:** All confounders included, correct specification
2. Run quantitative checks:
   ```python
   from causal_stats import (
       check_parallel_trends, check_common_support,
       balance_table,
   )
   ```
3. Output: per-assumption PASS / WARNING / FAIL verdicts
**Checkpoint:** Any FAIL (Type C) → present options: adjust method, add caveats, or abort

### `/causal sensitivity`
**Purpose:** Test how robust the estimate is to unmeasured confounding.
**Agent:** the `causal-sensitivity` plugin agent
**Flow:**
1. Run sensitivity analysis based on method:
   ```python
   from causal_stats import rosenbaum_bounds, e_value
   # PSM: rosenbaum_bounds(treated_outcomes, control_outcomes)
   # All: e_value(risk_ratio, ci_lower)
   ```
2. Translate to plain language: "An unmeasured confounder would need to be X times stronger than anything we measured to explain away this result."
3. Output: sensitivity report

### `/causal report`
**Purpose:** Generate a report with mandatory caveats.
**Agent:** the `causal-report-generator` plugin agent
**Flow:**
1. Compile: estimate + CI + assumption verdicts + sensitivity results
2. Place on confidence ladder (RCT > DiD+reg > PSM > DiD > regression > pre-post)
3. Include mandatory caveat block (method-specific, non-negotiable)
4. Output: `reports/causal_report_{{DATE}}.md`

### `/causal full`
**Purpose:** End-to-end: select → analyze → check → sensitivity → report.
**Flow:** Runs all modes in sequence. All Type C checkpoints fire.

## Confidence Ladder

Methods ranked by causal credibility (highest to lowest):

| Level | Method | Confidence |
|-------|--------|------------|
| 1 | RCT (Randomized Experiment) | **HIGH** |
| 2 | DiD + Regression Adjustment | **MODERATE-HIGH** |
| 3 | PSM (Good Overlap + Balance) | **MODERATE** |
| 4 | DiD (Parallel Trends OK) | **MODERATE** |
| 5 | Regression Adjustment | **LOW-MODERATE** |
| 6 | Pre-Post (With Trend) | **LOW** |
| 7 | Pre-Post (Simple) | **VERY LOW** |

## Mandatory Caveats (Non-Negotiable)

Every causal report MUST include the method-specific caveat. These are architecturally required — the agent cannot produce a report without them.

| Method | Mandatory Caveat |
|--------|-----------------|
| Pre-Post | "Assumes nothing else changed during this period. Any concurrent event could explain this result." |
| DiD | "Assumes the control group would have followed the same trend. Plausible but unprovable." |
| PSM | "Controls for observed confounders only. Unmeasured factors could bias this estimate." |
| Regression | "Assumes all relevant confounders are included and the model is correctly specified." |

## Helper Function Reference

| Function | Module | Use For |
|----------|--------|---------|
| `pre_post_analysis()` | `causal_stats.pre_post` | Pre-post comparison |
| `did_basic()` | `causal_stats.did` | 2x2 DiD estimator |
| `parallel_trends_test()` | `causal_stats.did` | Test parallel trends assumption |
| `event_study()` | `causal_stats.did` | Period-by-period effects |
| `propensity_match()` | `causal_stats.matching` | PSM pipeline |
| `balance_table()` | `causal_stats.balance` | SMD balance diagnostics |
| `love_plot()` | `causal_stats.balance` | Before/after balance visual |
| `regression_adjust()` | `causal_stats.regression` | OLS with covariates |
| `rosenbaum_bounds()` | `causal_stats.sensitivity` | PSM sensitivity |
| `e_value()` | `causal_stats.sensitivity` | Universal sensitivity measure |
| `check_parallel_trends()` | `causal_stats.assumptions` | DiD assumption |
| `check_common_support()` | `causal_stats.assumptions` | PSM assumption |

## Cross-Product Handoffs

- `/causal select` → "Can you randomize? YES" → suggest `/experiment design`
- `/experiment power` → NOT_VIABLE → suggest `/causal select`
- `/causal check` → All assumptions FAIL → suggest redesign or descriptive-only analysis

## State Management

```
analyses/{slug}/
├── causal_config.yaml       # Method selection + parameters (tracked)
├── working/                  # Intermediates (gitignored)
│   ├── causal_analysis_results.json
│   ├── assumption_report.md
│   └── sensitivity_report.md
└── reports/                  # Final reports (tracked)
    └── causal_report_{{DATE}}.md
```
