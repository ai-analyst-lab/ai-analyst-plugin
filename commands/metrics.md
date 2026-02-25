# Skill: Metrics

## Purpose
Browse, search, and display metric definitions from the active dataset's
metric dictionary. Provides quick access to how metrics are defined, computed,
and validated.

## When to Use
- User says `/metrics` or "show me the metrics" or "what metrics do we track?"
- During analysis, to confirm a metric's definition before computing it
- When writing a metric spec, to check for existing definitions

## Invocation
`/metrics` — list all metrics for the active dataset
`/metrics {id}` — show full spec for a specific metric
`/metrics category={cat}` — filter by category (e.g., monetization)
`/metrics search={term}` — search metric names and descriptions

## Instructions

### Step 1: Load Metric Dictionary
1. Read `.knowledge/active.yaml` to identify the active dataset.
2. Read `.knowledge/datasets/{active}/metrics/index.yaml` for the metric list.
3. If no metrics directory exists: "No metric dictionary for this dataset. Use the metric-spec skill to define metrics."

### Step 2: Execute Command

**List all (`/metrics`):**
- Display as a table: id, name, category, direction, validation_status
- Group by category
- Show total count

**Show specific (`/metrics {id}`):**
- Read `.knowledge/datasets/{active}/metrics/{id}.yaml`
- Display: name, category, owner, full definition (formula, unit, direction, granularity), source tables, dimensions, guardrails, typical range, validation status
- If metric not found: suggest closest match from index

**Filter by category (`/metrics category=monetization`):**
- Filter index by category field
- Display filtered table

**Search (`/metrics search=revenue`):**
- Search metric names and descriptions (case-insensitive substring)
- Display matching metrics

### Step 3: Contextual Suggestions
After displaying metrics, suggest relevant actions:
- "Want to validate {metric} against the current data? Use the data-profiling skill."
- "Need to define a new metric? Use the metric-spec skill."
- "Want to see how {metric} trends over time? Ask me to analyze it."

## Edge Cases
- **No active dataset:** Prompt to connect one
- **Empty metric dictionary:** Suggest using metric-spec skill
- **Metric referenced but not in dictionary:** Offer to create it
- **Stale validation:** Flag metrics where last_validated is >30 days ago
