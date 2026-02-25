# Skill: Compare Datasets

## Purpose
Compare metrics, findings, and patterns across two or more connected datasets.
Helps identify cross-dataset patterns (e.g., "conversion funnel behavior is
similar across both product lines") and dataset-specific anomalies.

## When to Use
- User says `/compare-datasets` or "compare across datasets"
- After analyzing multiple datasets, to find commonalities
- When the user asks "is this pattern unique to this dataset?"

## Invocation
`/compare-datasets` — compare active dataset with all others
`/compare-datasets {id1} {id2}` — compare two specific datasets
`/compare-datasets metric={name}` — compare a specific metric across datasets

## Instructions

### Step 1: Identify Datasets to Compare
1. Read `.knowledge/datasets/` to enumerate all connected datasets.
2. If specific datasets are named, validate they exist.
3. If no datasets specified, use active + all others.
4. Require at least 2 datasets. If only 1 exists: "Only one dataset connected. Use `/connect-data` to add another."

### Step 2: Load Metric Dictionaries
For each dataset:
1. Read `.knowledge/datasets/{id}/metrics/index.yaml`
2. Build a union of all metric IDs across datasets
3. Identify shared metrics (same ID or same name) vs. dataset-specific metrics

### Step 3: Compare Shared Metrics
For each metric that exists in 2+ datasets:
1. Load the metric YAML from each dataset
2. Compare: definition match? (same formula, same unit)
3. Compare: typical range overlap? (do the datasets have similar baselines?)
4. Compare: guardrails alignment? (are thresholds consistent?)
5. Flag discrepancies: "conversion_rate is defined differently in {dataset_a} vs {dataset_b}"

### Step 4: Compare Analysis History
For each dataset:
1. Read `.knowledge/analyses/index.yaml`
2. Extract key findings from recent analyses
3. Look for cross-dataset patterns:
   - Same finding appearing in multiple datasets
   - Opposite findings (metric up in one, down in another)
   - Same root cause identified independently

### Step 5: Generate Cross-Dataset Observations
Write findings to `.knowledge/global/cross_dataset_observations.yaml`:
- Shared patterns: behaviors that appear across datasets
- Divergences: where datasets behave differently
- Metric alignment: which metrics are consistently defined
- Suggested investigations: questions raised by the comparison

### Step 6: Present Results
Display a comparison table:

```
Cross-Dataset Comparison: {dataset_a} vs {dataset_b}

Shared Metrics: {N} ({M} with matching definitions)
Metric Discrepancies: {list}

Shared Patterns:
  - {pattern description} (seen in both datasets)

Divergences:
  - {metric} is {direction} in {dataset_a} but {direction} in {dataset_b}

Suggested Next:
  - "Investigate why {pattern} differs between datasets"
  - "Align {metric} definitions across datasets"
```

## Edge Cases
- **Only 1 dataset:** Cannot compare — suggest connecting another
- **No shared metrics:** Report this — datasets may serve different purposes
- **No analysis history:** Compare schemas and metric definitions only
- **Many datasets (>5):** Compare pairwise with the active dataset only
