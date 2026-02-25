# Skill: Datasets

## Purpose
List all connected datasets with their status, table counts, and last analysis date.

## When to Use
Invoke as `/datasets` when the user wants to see what datasets are available.

## Instructions

### Step 1: Read the source registry

Read `data_sources.yaml` to get the list of registered sources.

### Step 2: Read the active pointer

Read `.knowledge/active.yaml` to determine which dataset is currently active.

### Step 3: Enrich with brain data

For each registered source, check if `.knowledge/datasets/{name}/manifest.yaml` exists. If it does, read summary stats (table_count, date_range, analysis_count, last_used).

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

## Anti-Patterns

1. **Never show connection credentials** — display type and database/schema only, never tokens or passwords
2. **Never show datasets that have no registry entry** — orphaned .knowledge/datasets/ dirs without a data_sources.yaml entry should be ignored
