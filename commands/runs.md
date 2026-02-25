# Skill: Runs

## Purpose
Browse, inspect, compare, and clean up past pipeline runs. Each run is a
self-contained directory under `working/runs/` with its own working files,
outputs, and pipeline state.

## When to Use
- User says `/runs`, `/runs list`, `/runs latest`, `/runs clean`, or `/runs compare`
- When the user wants to see what analyses have been executed

## Invocation
- `/runs` or `/runs list` -- list all past runs
- `/runs latest` -- show details of the most recent run
- `/runs {id}` -- show details of a specific run (partial match supported)
- `/runs clean` -- remove runs older than 30 days (confirmation required)
- `/runs compare {id1} {id2}` -- compare two runs side by side

## Instructions

### Step 1: Scan Run Directory

Read `working/runs/` directory. Each subdirectory is a run, named:
```
{YYYY-MM-DD}_{DATASET}_{SHORT_TITLE}/
```

For each run directory, read `pipeline_state.json` to extract:
- `pipeline_id` -- timestamp identifier
- `dataset` -- dataset name
- `question` -- the business question
- `status` -- `completed`, `failed`, `paused`, or `running`
- `run_dir` -- full path
- `started_at`, `completed_at` -- timing
- `steps` -- agent status map (to compute agent counts)

If `pipeline_state.json` is missing, infer status as `unknown` and derive
date/dataset from the directory name.

### Step 2: Execute Command

**List (`/runs` or `/runs list`):**

Display a table sorted by date descending:

```
Pipeline Runs (working/runs/)

| # | Date       | Dataset   | Title                    | Status    | Agents |
|---|------------|-----------|--------------------------|-----------|--------|
| 1 | 2026-02-23 | acme-analytics | why-revenue-dropped-q3   | completed | 14/14  |
| 2 | 2026-02-21 | acme-analytics | activation-funnel-deep   | failed    | 8/14   |
| 3 | 2026-02-19 | hero      | churn-by-segment         | completed | 14/14  |

3 runs found. Use `/runs {#}` or `/runs {date_dataset_title}` for details.
```

The `Agents` column shows `{completed}/{total}` from the step map.

**Latest (`/runs latest`):**

Read `working/latest` symlink target. Display the detail view (same as `/runs {id}`).

**Detail (`/runs {id}`):**

Match `{id}` against run directory names (supports partial match -- e.g.,
`/runs acme-analytics` matches the most recent acme-analytics run). Display:

```
Run: {directory_name}
Status: {status}
Dataset: {dataset}
Question: {question}
Started: {started_at}
Completed: {completed_at} ({duration})

Agent Status:
  completed: {list}
  failed: {list with errors}
  skipped: {list}
  pending: {list}

Output Files:
  - {RUN_DIR}/outputs/{file1}
  - {RUN_DIR}/outputs/{file2}
  ...

Confidence: {grade from validation if available}
```

If the run has a validation report, extract and show the confidence grade.

**Clean (`/runs clean`):**

1. Identify runs older than 30 days (based on directory date prefix)
2. List them and ask for confirmation:
   ```
   Found {N} runs older than 30 days:
     - {dir1} (completed, {date})
     - {dir2} (failed, {date})

   Delete these runs? This cannot be undone. [y/N]
   ```
3. On confirmation, remove the directories
4. If `working/latest` pointed to a deleted run, remove the symlink

**Compare (`/runs compare {id1} {id2}`):**

Load `pipeline_state.json` and key output files from both runs. Display:

```
Comparing Runs:
  A: {dir1}
  B: {dir2}

| Dimension          | Run A              | Run B              |
|--------------------|--------------------|--------------------|
| Date               | {date_a}           | {date_b}           |
| Dataset            | {dataset_a}        | {dataset_b}        |
| Status             | {status_a}         | {status_b}         |
| Agents completed   | {count_a}          | {count_b}          |
| Confidence grade   | {grade_a}          | {grade_b}          |
| Charts generated   | {chart_count_a}    | {chart_count_b}    |
| Key findings       | {finding_count_a}  | {finding_count_b}  |
| Duration           | {duration_a}       | {duration_b}       |
```

If both runs analyzed the same dataset, also compare:
- Top 3 findings from each (extracted from analysis reports)
- Any metrics that differ significantly

## Edge Cases
- **No runs directory:** Report "No pipeline runs found. Use `/run-pipeline` to start one."
- **Empty runs directory:** Same message as above
- **Corrupted pipeline_state.json:** Show run with `status: unknown`, note the error
- **Partial match ambiguity:** If multiple runs match, list them and ask user to be more specific
- **Legacy runs (no run directory):** Note: "Found legacy `working/pipeline_state.json` -- not in per-run format. Use `/run-pipeline` to create a tracked run."
