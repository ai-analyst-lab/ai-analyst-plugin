# Skill: Log Correction

## Purpose
Record analyst mistakes and their fixes so future analyses learn from past
errors. Manual counterpart to automatic feedback capture.

## When to Use
- User says "log a correction", "that was wrong because...", or similar
- Feedback-capture skill routes here for detailed correction entry
- After discovering and fixing an error mid-analysis

## Instructions

### Step 1: Gather Details

Extract from conversation context or ask the user:

1. **What was wrong?** — One-sentence description of the error
2. **What is the correct answer?** — The fix or corrected approach
3. **Which dataset/tables?** — Dataset name and affected table(s)
4. **How severe?** — `critical` (wrong numbers shared) | `high` (changes conclusions) | `medium` (directionally correct) | `low` (no impact)
5. **SQL before/after?** — If the error involved a query, capture both versions

If any required field is unclear, ask the user. Do not guess severity.

### Step 2: Categorize

Assign one category based on the error type:

| Category | Description |
|----------|-------------|
| `sql` | Wrong query — bad join, missing filter, incorrect aggregation |
| `metric` | Wrong metric definition — numerator/denominator error, wrong time window |
| `schema` | Wrong column or table reference — stale schema, misnamed field |
| `logic` | Flawed reasoning — Simpson's paradox missed, survivorship bias, wrong comparison |
| `other` | Anything that does not fit the above |

### Step 3: Write the Correction

1. Read `.knowledge/corrections/index.yaml` using `safe_read_yaml()`
2. Derive next ID: if `last_correction_id` is null, use `CORR-001`; otherwise
   parse the numeric suffix, increment, and zero-pad to 3 digits
3. Build the entry following `.knowledge/corrections/log.template.yaml`:

```yaml
- id: "CORR-{N}"
  date: "{YYYY-MM-DD}"
  severity: "{severity}"
  category: "{category}"
  dataset: "{dataset_name}"
  tables: ["{table1}", "{table2}"]
  description: "{what was wrong}"
  fix: "{what the correct approach is}"
  sql_before: "{original query, if applicable, else null}"
  sql_after: "{corrected query, if applicable, else null}"
  prevented_by: "{which validation layer should have caught this}"
```

4. Read `.knowledge/corrections/log.yaml` using `safe_read_yaml()`
5. Append the new entry to the `corrections` list
6. Write back using `atomic_write_yaml()`

### Step 4: Update Index

1. Read `.knowledge/corrections/index.yaml` (already loaded in Step 3)
2. Increment `total_corrections`
3. Increment the matching `by_severity.{severity}` counter
4. Increment `by_category.{category}` (create the key if it does not exist)
5. Set `last_correction_id` to the new ID
6. Set `last_updated` to today's date
7. Write back using `atomic_write_yaml()`

### Step 5: Confirm

Report to the user:

```
Correction logged: {id}
  Severity: {severity} | Category: {category}
  Description: {description}
  Fix: {fix}

Future analyses will check for this pattern during validation.
```

## Rules
1. Never overwrite existing corrections -- always append
2. Always read current state before writing (no blind overwrites)
3. If `log.yaml` or `index.yaml` is missing or corrupt, create from scratch
   with schema_version 1
4. SQL snippets in `sql_before`/`sql_after` should be trimmed to the relevant
   clause, not the entire multi-hundred-line query
5. `prevented_by` should reference a specific validation layer: structural,
   logical, business-rules, Simpson's check, or source tie-out

## Edge Cases
- **No SQL involved:** Set `sql_before` and `sql_after` to null
- **Dataset unknown:** Set `dataset` to "unknown" and note in description
- **Duplicate correction:** Still log it -- repeated errors signal a systemic gap
- **Correction to a correction:** Log as a new entry referencing the prior ID in description
