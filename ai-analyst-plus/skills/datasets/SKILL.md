---
name: datasets
description: >-
  List all connected datasets with status, table counts, and last analysis date, and switch the
  active dataset. Trigger on "/datasets", "/switch-dataset", "what datasets do I have?", "show me
  my data sources", "list datasets", "which datasets are connected?", "what data is available?",
  "switch dataset", "change dataset", "what's my active dataset?". Offer proactively when the user
  seems unsure what data they are working with.
---

# Skill: Datasets

## Purpose
List all connected datasets with their status, table counts, and last analysis date. Also owns the switch procedure: `/switch-dataset` changes which dataset is active.

## When to Use
Invoke as `/datasets` when the user wants to see what datasets are available, and as `/switch-dataset {name}` (or "switch to the other dataset") to change the active dataset.

## Instructions

### Step 1: Discover available datasets

The system supports two discovery paths:

**Path A: Registry-first** (preferred)
- Read `data_sources.yaml` to get the official list of registered sources
- If the file exists and has entries, use this as your source of truth

**Path B: Brain-first** (fallback when registry is empty)
- If `data_sources.yaml` is empty or missing, scan `.knowledge/datasets/` directory
- Each subdirectory represents a dataset (directory name = dataset ID)
- Read each dataset's `manifest.yaml` to get connection details and metadata

Use whichever path yields results. Many installations have datasets in `.knowledge/datasets/` but an empty `data_sources.yaml` registry — this is normal during initial setup or when datasets are added manually.

### Step 2: Read the active pointer

Read `.knowledge/active.yaml` to determine which dataset is currently active.

### Step 3: Enrich with manifest data

For each discovered dataset (whether from registry or directory scan), read `.knowledge/datasets/{name}/manifest.yaml` to get:
- `display_name` — human-readable name
- `connection.type` — connection type (csv, local_duckdb, snowflake, postgres, bigquery)
- `connection.database` or other connection-specific fields
- `last_profiled`: when the dataset was last profiled (null until data-profiling runs)

Table counts, date ranges, and row counts come from the dataset's `schema.md` or `last_profile.md` when those exist; connect-data's registration writes none of them. If a manifest is missing or those files have not been written yet, show what you can determine from the directory structure and note that the dataset needs profiling.

### Step 4: Display the list

```
Connected Datasets:

  * your_dataset (active)
    Your Dataset Name — {table_count} tables, {date_range}
    Connection: {type} ({database})
    Analyses: 0

  - {other_dataset}
    {display_name} — {table_count} tables, {date_range}
    Connection: {type} ({details})
    Analyses: {count}

Commands:
  /switch-dataset {name}  — switch active dataset
  /connect-data           — connect a new dataset
  /data                   — inspect active dataset schema
```

Mark the active dataset with `*`. Mark others with `-`.

### Switching the active dataset (`/switch-dataset`)

`/switch-dataset {name}`, "switch dataset", "change dataset", and "use the other dataset" all resolve here. This is the only switch procedure; other skills that mention `/switch-dataset` mean this section.

1. **Resolve the target.** Match `{name}` case-insensitively against the discovered dataset ids and display names (Step 1). If no name was given and exactly one non-active dataset exists, propose it; otherwise show the list and ask which one.
2. **No match:** say so, list the available ids, and suggest `/connect-data` for a new source. Write nothing.
3. **Already active:** say "{name} is already the active dataset" and stop.
4. **Confirm, then write.** Confirm the switch with the user ("Switch active dataset from {active} to {name}?"), then update `.knowledge/active.yaml` so `active_dataset: {id}` points at the target. Preserve any other keys in the file.
5. **Reload context.** Confirm the new active dataset to the user and reload session context per the knowledge-bootstrap skill (its "after /connect-data or /switch-dataset" rule): the target's schema.md, quirks.md, metrics, and corrections now apply.

If the user's request came bundled with an analysis question ("switch to the Q3 file and rerun the trend"), do the switch first, then continue the analysis against the new active dataset.

## Important Notes

1. **Security**: Never display connection credentials (tokens, passwords, API keys) — show only connection type and database/schema names
2. **Discovery**: If `data_sources.yaml` is empty but `.knowledge/datasets/` has content, scan the directory and show what's available — this is a normal state during development or manual dataset setup
3. **Incomplete manifests**: If a dataset directory exists but has no manifest or an incomplete manifest, include it in the list with status "Not yet profiled" and show whatever metadata is available
4. **Duplicate detection**: If you notice two datasets pointing to the same underlying data (same path or same database), mention this in a Notes section to help users clean up
