# Skill: Switch Dataset

## Purpose
Change the active dataset. Updates the active pointer, validates the target dataset exists, and confirms with a summary of what's now active.

## When to Use
Invoke as `/switch-dataset {name}` when the user wants to analyze a different dataset than the currently active one.

## Instructions

### Step 1: Validate the target dataset

1. Read `data_sources.yaml` to check if `{name}` exists as a registered source
2. If not found, try fuzzy matching (case-insensitive, partial match)
3. If still not found, list available datasets and ask user to choose

### Step 2: Validate the data brain exists

1. Check that `.knowledge/datasets/{name}/manifest.yaml` exists
2. If it doesn't exist, suggest: "Dataset '{name}' is registered but has no data brain. Run `/connect-data` to set it up."

### Step 3: Update the active pointer

1. Read `.knowledge/active.yaml`
2. Update `active_dataset` to `{name}`
3. Append to `switch_history` (cap at 20 entries, FIFO)
4. Write updated `.knowledge/active.yaml`

### Step 4: Confirm the switch

Read the target dataset's `manifest.yaml` and display:

```
Switched to: {display_name}
Tables: {table_count}
Date range: {date_range}
Connection: {connection.type} ({connection.database}.{connection.schema})
Last analysis: {last_used or "none"}
Metrics defined: {count from metrics/index.yaml or 0}
```

## Anti-Patterns

1. **Never silently switch** — always confirm with a summary
2. **Never switch mid-analysis** — if working/ has artifacts from the previous dataset, warn: "You have in-progress work for {old_dataset}. Switch anyway?"
3. **Never infer the dataset** — only switch when explicitly requested via this skill
