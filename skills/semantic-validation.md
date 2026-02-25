# Skill: Semantic Validation

## Purpose
Orchestrate the full 4-layer validation stack plus confidence scoring to
produce a comprehensive data quality assessment for any analysis output.

## When to Use
- After analysis agents produce findings (before Storytelling agent)
- When the Validation agent runs its enhanced checks (Step 5a-5e)
- When a user asks "how confident should I be in these results?"

## Invocation
Applied automatically as part of the Validation agent workflow. Can also
be invoked standalone: "Validate the quality of this analysis."

## Instructions

### Layer 1: Structural Validation
Use `helpers/structural_validator.py`:

```python
from helpers.structural_validator import (
    validate_schema, validate_primary_key,
    validate_referential_integrity, validate_completeness
)

# Check schema matches expected structure
schema_result = validate_schema(df, expected_columns, expected_types)

# Check primary key uniqueness
pk_result = validate_primary_key(df, key_columns)

# Check FK references exist in parent table
ri_result = validate_referential_integrity(child_df, parent_df, fk_column, pk_column)

# Check column completeness (null rates)
completeness_result = validate_completeness(df, thresholds={"warn": 0.05, "fail": 0.20})
```

Flag any FAIL results as BLOCKER — analysis built on broken data is invalid.

### Layer 2: Logical Validation
Use `helpers/logical_validator.py`:

```python
from helpers.logical_validator import (
    validate_aggregation_consistency, validate_trend_continuity,
    validate_segment_exhaustiveness, validate_temporal_consistency
)

# Parts must sum to whole
agg_result = validate_aggregation_consistency(parts_df, total_value, tolerance=0.01)

# No discontinuities in time series
trend_result = validate_trend_continuity(ts_df, date_col, value_col, max_gap_days=7)

# Segments must cover the full population
seg_result = validate_segment_exhaustiveness(segment_df, total_count)

# Date ranges across tables must overlap
temporal_result = validate_temporal_consistency(tables_dict, date_columns)
```

WARN on logical inconsistencies — they suggest calculation errors.

### Layer 3: Business Rules Validation
Use `helpers/business_rules.py`:

```python
from helpers.business_rules import (
    validate_ranges, validate_rates, validate_yoy_change
)

# Check values fall within plausible ranges
range_result = validate_ranges(df, column, min_val, max_val)

# Check rates are 0-100% and denominators > 0
rate_result = validate_rates(numerator, denominator)

# Check YoY changes are plausible (not 10000%)
yoy_result = validate_yoy_change(current, previous, max_change_pct=500)
```

Flag implausible values as WARN — they may be correct but need explanation.

### Layer 4: Simpson's Paradox Check
Use `helpers/simpsons_paradox.py`:

```python
from helpers.simpsons_paradox import check_simpsons_paradox, scan_dimensions

# Check a specific aggregate vs segment breakdown
paradox = check_simpsons_paradox(df, metric_col, segment_col)

# Scan multiple dimensions for paradox risk
scan = scan_dimensions(df, metric_col, dimension_cols)
```

BLOCKER on confirmed paradox — the aggregate finding is misleading.

### Confidence Scoring
After all 4 layers complete, synthesize results into a confidence score:

```python
from helpers.confidence_scoring import score_confidence, format_confidence_badge

# Collect all validation results
validation_results = {
    "structural": [schema_result, pk_result, ri_result, completeness_result],
    "logical": [agg_result, trend_result, seg_result, temporal_result],
    "business_rules": [range_result, rate_result, yoy_result],
    "simpsons_paradox": [paradox_result],
    "sample_size": len(df)
}

score = score_confidence(validation_results)
badge = format_confidence_badge(score)

# score returns: {score: 0-100, grade: A-F, factors: {...}, flags: [...]}
# badge returns: "A (92/100)" or "C (58/100) — 2 warnings"
```

### Output Integration
Pass the confidence score and badge to downstream agents:
- **Storytelling agent**: Include badge in executive summary
- **Deck Creator**: Show badge on synthesis slide
- **Validation report**: Full factor breakdown in the validation report

### Severity Mapping
| Layer | FAIL → | WARN → |
|-------|--------|--------|
| Structural | BLOCKER (halt analysis) | WARNING (proceed with caution) |
| Logical | WARNING (check calculations) | INFO (note in report) |
| Business Rules | WARNING (explain outliers) | INFO (note in report) |
| Simpson's | BLOCKER (disaggregate) | WARNING (check segments) |

## Edge Cases
- **Missing validators**: If a helper module is unavailable, skip that layer
  and cap confidence at grade C
- **Empty data**: Structural validation catches this — BLOCKER before other
  layers run
- **Single-table analysis**: Skip referential integrity and segment
  exhaustiveness checks
- **No time dimension**: Skip temporal consistency and trend continuity checks
