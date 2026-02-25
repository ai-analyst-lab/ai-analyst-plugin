# Skill: Explore Data

## Purpose
Quick, interactive data exploration without the full pipeline. Lets users
poke around the active dataset — preview tables, check distributions, spot
patterns, and form hypotheses before committing to a formal analysis.

## When to Use
- User says `/explore` or "let me explore the data" or "what's in this dataset?"
- After connecting a new dataset, before any formal analysis
- When the user wants to understand data shape without a specific question

## Invocation
`/explore` — explore the active dataset
`/explore {table}` — focus on a specific table
`/explore {table} {column}` — deep-dive into a specific column

## Instructions

### Step 1: Load Context
Read `.knowledge/active.yaml` to identify the active dataset.
Read `.knowledge/datasets/{active}/schema.md` for table/column reference.
Read `.knowledge/datasets/{active}/quirks.md` for known gotchas.

If no active dataset, prompt: "No dataset connected. Use `/connect-data` to add one."

### Step 2: Choose Exploration Mode

**Mode A: Dataset overview** (no table specified)
- List all tables with row counts and date ranges
- Highlight the 3-5 most analytically useful tables (most rows, most joins)
- Show key entities and how they connect
- Suggest 3 starting questions based on available data

**Mode B: Table exploration** (table specified)
- Show column list with types and null rates
- Sample 5 random rows
- For numeric columns: min, max, mean, median
- For categorical columns: top 5 values with counts
- For date columns: range and coverage
- Flag any quality issues (>5% nulls, low cardinality, suspicious values)

**Mode C: Column deep-dive** (table + column specified)
- Full distribution: histogram for numeric, bar chart for categorical
- Null analysis: count, pattern (random vs systematic)
- Outlier detection: IQR method, flag extremes
- If date column: coverage heatmap by week
- Suggest related columns for cross-analysis

### Step 3: Interactive Follow-Up
After presenting results, offer 2-3 contextual next actions:
- "Want to see how {column} varies by {dimension}?"
- "This looks like a good candidate for funnel analysis. Want to try `/run-pipeline`?"
- "There are quality issues in {column}. Want to run `/data-profiling`?"

### Step 4: Save Exploration Notes
Write a brief exploration summary to `working/explore_notes_{DATE}.md`:
- Tables examined
- Key observations
- Quality flags
- Suggested next steps

This file is available for subsequent agents (e.g., Question Framing can reference
exploration notes to inform hypothesis generation).

## Rules
1. Keep it fast — no more than 3-4 queries per exploration step
2. Always apply `swd_style()` if generating any chart
3. Never modify data during exploration
4. Always cite table and column names in output
5. If data source is CSV fallback, mention this to the user

## Edge Cases
- **Empty table:** Report row count = 0, suggest checking data load
- **Table not found:** Fuzzy-match against schema, suggest closest match
- **Column has all nulls:** Flag as BLOCKER, suggest checking data pipeline
- **Very wide table (>50 columns):** Group columns by category, show summary not full list
