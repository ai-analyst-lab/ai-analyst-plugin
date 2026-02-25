# Skill: Archive Analysis

## Purpose
Save a completed analysis to the knowledge system's analysis archive for
future recall. Captures key findings, metrics used, agents invoked, and
output file paths so that past work can be referenced in future sessions.

## When to Use
- After completing an L3+ analysis (post-validation)
- After `/run-pipeline` completes successfully
- User says "save this analysis" or "archive this"
- Automatically triggered at the end of Step 18 (Close the Loop)

## Instructions

### Step 1: Gather Analysis Metadata
Collect from the current session:

1. **Title:** Derive from the original question or business context
2. **Question:** The original user question
3. **Question level:** From the Question Router classification (L1-L5)
4. **Dataset ID:** From `.knowledge/active.yaml`
5. **Key findings:** Extract top 3-5 findings from the analysis output
   or validation report
6. **Metrics used:** List metric IDs referenced during analysis (match
   against metric dictionary if available)
7. **Agents used:** List agent names that were invoked
8. **Output files:** List paths to files in `outputs/` and `working/`
9. **Tags:** Auto-generate from question keywords + metric names
10. **Confidence:** From the validation agent's confidence score, if available

### Step 2: Create Archive Entry
Generate a unique ID: `analysis_{YYYYMMDD}_{HHMMSS}`

Build the entry dict following `.knowledge/analyses/_schema.yaml`.

### Step 3: Append to Index
1. Read `.knowledge/analyses/index.yaml`
2. Append the new entry to the `analyses` list
3. Increment `total_analyses`
4. Update `last_updated` to current date
5. Write back to `index.yaml`

### Step 4: Update Dataset Stats
1. Read `.knowledge/datasets/{active}/manifest.yaml`
2. Increment `analysis_count`
3. Update `last_used` to current date
4. Write back

### Step 5: Confirm
Report to user:
```
Analysis archived: {title}
ID: {id}
Findings: {count} key findings captured
Use `/history` to browse past analyses.
```

### Step 6: Capture to Query Archaeology (Optional)

After archiving, check if the analysis produced reusable patterns worth saving
to `.knowledge/query-archaeology/curated/` via `helpers/archaeology_helpers.py`.

1. **SQL patterns** — If validated SQL queries could be reused for future analyses:
   - Offer to capture via `capture_cookbook_entry(title, sql, dataset, tables, tags)`
   - Only capture queries that passed tie-out or validation checks

2. **Table knowledge** — If the analysis revealed useful table metadata:
   - Offer to capture/update via `capture_table_cheatsheet(table_name, dataset, grain, primary_key, common_filters, gotchas, common_joins)`
   - Include grain, primary key, common filters, gotchas, and common joins

3. **Join patterns** — If the analysis used non-obvious joins:
   - Offer to capture via `capture_join_pattern(tables, join_sql, cardinality, validated, dataset)`
   - Record cardinality and whether the join was validated

**Rules for this step:**
- Ask the user: "Would you like to save any SQL patterns from this analysis?"
- If the user declines or there are no reusable patterns, skip silently
- Only capture patterns from analyses with confidence grade B or better
- Never auto-capture without user confirmation

## Rules
1. Never overwrite an existing archive entry — always append
2. Key findings should be one sentence each, factual, with numbers
3. Tags should be lowercase, no spaces (use hyphens)
4. If validation was not run, set confidence to null and note it
5. Archive even partial analyses — mark as `partial: true`

## Edge Cases
- **No outputs exist:** Archive with metadata only, note "no output files"
- **Pipeline was interrupted:** Archive what's available, mark as partial
- **Duplicate question:** Still archive — different runs may find different things
- **Analysis index doesn't exist:** Create it from template
