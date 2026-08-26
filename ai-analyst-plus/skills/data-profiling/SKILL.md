---
name: data-profiling
description: >-
  Deep-profile the active dataset: distributions, temporal patterns, correlations, completeness
  gaps, anomalies. Use after connecting a new dataset. Trigger on "profile this data",
  "deep-profile the dataset", "run a data profile", "check distributions", "find anomalies in the
  data", "how complete is this data". For a first-contact overview use data-map; for one column
  use distribution-profiler; for schema use data-inspect.
---

# Skill: Data Profiling

## Purpose
Deep-profile the active dataset to understand schema structure, value distributions, temporal patterns, correlations, completeness gaps, and anomalies. Produces a comprehensive profile report that serves as the foundation for analysis planning and data quality assessment.

**Bundled profiling library:** the profiling functions used below ship inside this skill at `scripts/` (`data_helpers.py`, `schema_profiler.py`, `deep_profiler.py`; pandas/numpy, plus duckdb for DuckDB sources). Add this skill's `scripts/` directory to `sys.path` before the imports in the steps below:

```python
import sys
import pandas as pd
sys.path.insert(0, "<path to this skill>/scripts")  # the scripts/ dir next to this SKILL.md
```

**If the skill install path cannot be resolved** (some sandboxed environments): read the script file(s) from this skill, write a copy into a `scripts/` folder inside the working folder, and run from there. The scripts are self-contained.

Run Python from the working folder root so `.knowledge/` paths resolve.

## When to Use
- After connecting a new dataset (post-bootstrap, pre-analysis)
- Before the first analysis on any dataset
- When explicitly invoked by the user
- When the existing profile is stale (check `last_profiled` in manifest.yaml)

**DISAMBIGUATION:** this is the DEEP statistical profile (distributions, correlations, anomalies). For cross-table relationships/health and the first-contact "tell me about this data" overview, use `data-map`; for a single column's distribution, use `distribution-profiler`; for a plain schema listing, use `/data` (data-inspect).

## Instructions

### Step 1: Connect and Profile Schema

```python
from data_helpers import get_connection_for_profiling
from schema_profiler import profile_source

# Get connection (auto-detects DuckDB vs CSV from active dataset)
conn_info = get_connection_for_profiling()

# Run full schema profile — introspects all tables: column names, types,
# nullability, row counts, sample values, basic statistics, date detection
schema = profile_source(conn_info)
```

Record the output. `schema` contains the full table inventory with column-level metadata. Use this to identify:
- Which tables exist and their row counts
- Which columns are date columns (for temporal analysis in Step 2)
- Which columns are numeric (for distribution and correlation analysis)
- Which columns have nulls (for completeness deep-dive in Step 2)

### Step 2: Run Deep Profiling per Table

For each table in the schema, load the data and run the deep profiling functions. Prioritize tables with the most rows and the most date/numeric columns.

```python
from data_helpers import read_table
from deep_profiler import (
    profile_distributions,
    profile_temporal_patterns,
    profile_completeness,
)

for table_info in schema["tables"]:
    table_name = table_info["name"]
    df = read_table(table_name)

    # Distribution analysis on all numeric columns
    distributions = profile_distributions(df)

    # Completeness assessment — null rates, zeros, empty strings, constant cols
    completeness = profile_completeness(df)

    # Temporal pattern analysis (only if the table has date columns)
    temporal = None
    if table_info.get("date_columns"):
        primary_date = table_info["date_columns"][0]
        temporal = profile_temporal_patterns(df, primary_date, freq="D")
```

**Important:** For large tables (>50K rows), `profile_source()` already samples. But `read_table()` loads the full CSV. If a table has >100K rows, sample before running deep profiling:

```python
if len(df) > 100_000:
    df = df.sample(n=100_000, random_state=42)
```

### Step 3: Correlation and Anomaly Analysis on Key Tables

Run correlation and anomaly detection on tables that contain key business metrics (revenue, counts, rates). Identify these tables by looking for columns with names like `revenue`, `amount`, `total`, `count`, `rate`, `price`, `quantity`.

```python
from deep_profiler import profile_correlations, profile_anomalies

# Correlations — find relationships between numeric columns
correlations = profile_correlations(df, threshold=0.5)

# Anomaly detection — requires a date column and pre-aggregated data.
# Aggregate to daily granularity first if the table has event-level rows.
if table_info.get("date_columns"):
    primary_date = table_info["date_columns"][0]
    # Only run on tables with a clear date + metric pattern
    metric_cols = [c for c in df.select_dtypes(include="number").columns
                   if c not in ("id", table_name.rstrip("s") + "_id")]
    if metric_cols:
        # Daily mean of each metric. Use .sum() for daily totals, or a
        # separate .size() aggregation when you want daily row volume.
        daily = (
            df.groupby(pd.to_datetime(df[primary_date]).dt.date)[metric_cols]
              .mean()
              .reset_index()  # the date returns as a column named {primary_date}
        )
        anomalies = profile_anomalies(daily, date_col=primary_date,
                                      metric_cols=metric_cols, window=14)
        # Fail loudly on an empty scan — a profile with a silently empty
        # Anomalies section is worse than an error.
        if anomalies["metrics_scanned"] == 0:
            raise RuntimeError(
                f"Anomaly scan for {table_name} scanned zero metrics: "
                f"{anomalies['summary']} Fix the aggregation before writing the report."
            )
```

### Step 4: Generate Profile Report

Write the full profile report to `.knowledge/datasets/{active}/last_profile.md`. Use `schema_to_markdown()` for the schema portion, then append the deep profiling results.

```python
from data_helpers import schema_to_markdown, detect_active_source

source = detect_active_source()
active_dataset = source["source"]

# Build the schema markdown section
schema_md = schema_to_markdown(schema)
```

Assemble the full report and write it to:
```
.knowledge/datasets/{active_dataset}/last_profile.md
```

Then update the manifest: set `last_profiled` in
`.knowledge/datasets/{active_dataset}/manifest.yaml` to today's date. This skill owns that
field; it is what the staleness check in "When to Use" reads.

## Output Format

```markdown
# Data Profile: {dataset_name}
**Profiled at:** {ISO timestamp}
**Source:** {connection type} ({path or schema prefix})
**Tables:** {count}  |  **Total rows:** {sum}

---

## Summary of Findings

| Severity | Count | Details |
|----------|-------|---------|
| BLOCKER  | X     | {brief list} |
| WARNING  | X     | {brief list} |
| INFO     | X     | {brief list} |

---

## Schema Overview

{output of schema_to_markdown()}

---

## Distribution Analysis

### {table_name}

| Column | Shape | Skewness | Outliers (IQR) | Recommended Transform |
|--------|-------|----------|----------------|----------------------|
| {col}  | {shape} | {skew} | {n_outliers}  | {transform or "none"} |

---

## Temporal Patterns

### {table_name} ({date_column})

- **Date range:** {min} to {max}
- **Coverage:** {actual}/{expected} periods ({pct}%)
- **Gaps:** {count} gaps found {list if any}
- **Trend:** {trend direction}
- **Seasonality:** {detected or not}
- **Day-of-week pattern:** {summary}

---

## Completeness

### {table_name}

| Column | Status | Null % | Zeros | Empty Strings | Constant? |
|--------|--------|--------|-------|---------------|-----------|
| {col}  | {status} | {pct} | {count} | {count}    | {yes/no}  |

---

## Correlations

### {table_name}

| Column A | Column B | Correlation | Strength | Direction |
|----------|----------|-------------|----------|-----------|
| {col_a}  | {col_b}  | {r}         | {strength} | {direction} |

---

## Anomalies

### {table_name}

{anomaly summary}

| Metric | Spikes | Drops | Details |
|--------|--------|-------|---------|
| {metric} | {count} | {count} | {top anomalies with dates} |

---

## Recommendations

- **BLOCKER items:** {must fix before analysis}
- **WARNING items:** {note as caveats}
- **Suggested analysis focus:** {tables/columns with most signal}
```

### Severity Classification

Apply these rules consistently across all sections:

| Severity | Condition |
|----------|-----------|
| **BLOCKER** | >50% nulls in a key metric column; entire date ranges missing (coverage <50%); constant columns that should have variance; very strong correlations (r>0.95) suggesting duplicate columns |
| **WARNING** | 5-50% nulls; heavy-tailed or bimodal distributions in metric columns; date coverage 50-90%; moderate anomalies detected; skewness >3 suggesting data quality issues |
| **INFO** | <5% nulls; normal or mild skew distributions; full date coverage; no anomalies; expected correlations (e.g., quantity and revenue) |

## Edge Cases

1. **No date columns in any table:** Skip temporal analysis and anomaly detection entirely. Note in the report: "No temporal columns detected -- temporal analysis skipped."
2. **Single-column tables or lookup tables:** Run completeness only. Skip distributions, correlations, and anomalies. Flag as "lookup table" in the report.
3. **All columns are non-numeric:** Skip distribution and correlation analysis. Focus on completeness and categorical cardinality.
4. **Very wide tables (>50 columns):** Profile all columns for completeness, but limit distribution analysis to the top 20 numeric columns by variance. Note which columns were skipped.
5. **Empty tables (0 rows):** Log as BLOCKER. Do not attempt profiling -- report the table as empty and move on.
6. **DuckDB connection fails:** Fall back to CSV via `read_table()`. The schema profiler handles this internally, but deep profiling should also use the CSV path.

## Anti-Patterns

1. **Never skip profiling because "the data looks clean."** Surprises hide in distributions and temporal patterns that summary stats miss.
2. **Never run anomaly detection on raw event rows.** Always aggregate to daily or weekly granularity first. Running on raw rows will flag every row as an "anomaly" relative to rolling stats.
3. **Never profile in isolation from schema context.** Always run `profile_source()` first (Step 1) so you know which columns are dates, which are numeric, and what the cardinality looks like before deep profiling.
4. **Never treat all WARNING items equally.** A 10% null rate in a segmentation column is more impactful than 10% nulls in a free-text notes column. Contextualize severity by the column's role in analysis.
5. **Never skip the report write.** Even if profiling runs smoothly, always write `last_profile.md` so future sessions can reference it without re-profiling.
