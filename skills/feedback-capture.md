# Skill: Feedback Capture

## Purpose
Pre-router interceptor that runs BEFORE the Question Router on every user
message. Detects correction signals, methodology learnings, and positive
feedback, captures them to `.knowledge/`, then passes through to normal routing.

## When to Use
- On every incoming user message, before Question Router classification
- Runs silently — the user should never notice this skill executing

## Instructions

### Step 0: Intercept (runs before Question Router)

Wrap all detection and capture logic in try/except. If anything fails, log
nothing and pass the message through to the Question Router unchanged. Never
block the pipeline.

### Step 1: Detect feedback type

Scan the user's message for these signal patterns:

**Correction signals** (user says something was wrong):
- "that's wrong", "that's incorrect", "actually it's...", "it should be..."
- "the column is X not Y", "that number should be...", "you used the wrong..."
- "off by...", "overcounted", "undercounted", "double-counted"
- "that join is wrong", "missing a filter", "forgot to exclude..."

**Learning signals** (user teaches a reusable methodology):
- "next time...", "always use...", "never use...", "prefer X over Y"
- "the convention here is...", "our team uses...", "don't forget to..."
- "a better approach would be...", "going forward...", "remember that..."

**Positive signals** (user confirms correctness):
- "that's right", "exactly", "perfect", "good analysis", "looks good"

**No signal**: No pattern matched. If multiple match, prioritize: Correction > Learning > Positive.

### Step 2: Act on detection

#### If Correction detected:

1. Read `.knowledge/corrections/index.yaml` to get `last_correction_id`.
2. Compute next ID: increment the numeric suffix (e.g., `CORR-001` -> `CORR-002`).
   If `last_correction_id` is null, start at `CORR-001`.
3. Estimate severity from context:
   - **critical**: Wrong conclusion presented to stakeholders
   - **high**: Wrong numbers in output, incorrect joins affecting results
   - **medium**: Wrong column, filter, or metric definition used
   - **low**: Minor label, formatting, or naming issue
4. Classify category: `join_error` | `filter_missing` | `metric_definition` |
   `date_range` | `aggregation` | `schema` | `logic` | `other`
5. Read `.knowledge/corrections/log.yaml`.
6. Append a new entry to the `corrections` list:
   ```yaml
   - id: "CORR-{N}"
     date: "{TODAY}"
     severity: "{estimated}"
     category: "{classified}"
     dataset: "{active dataset or null}"
     tables: []
     description: "{what the user said was wrong}"
     fix: "{what the user said is correct}"
     sql_before: null
     sql_after: null
     prevented_by: null
   ```
   Fill `tables`, `sql_before`, `sql_after`, and `prevented_by` only if the
   user's message contains enough detail. Leave null otherwise.
7. Write updated `log.yaml`.
8. Update `.knowledge/corrections/index.yaml`: increment `total_corrections`,
   increment the matching `by_severity` and `by_category` counts, set
   `last_correction_id` and `last_updated`.
9. Acknowledge briefly: "Got it, logged as {ID}." Then continue processing
   the user's underlying request normally.

#### If Learning detected:

1. Read `.knowledge/learnings/index.md`.
2. Classify into one of the six categories:
   - Data Patterns | Query Techniques | Business Context |
     Stakeholder Preferences | Visualization Insights | Methodology Notes
3. Append a bullet point under the matching `### {N}. {Category}` heading.
   Format: `- {concise learning} (source: user feedback, {TODAY})`
4. Write updated `index.md`.
5. Acknowledge briefly: "Noted for future analyses." Then continue processing
   the user's underlying request normally.

#### If Positive feedback detected:

Acknowledge briefly ("Thanks!" or similar one-liner) and continue processing
the rest of the message normally. No file writes needed.

#### If No signal detected:

Pass through silently. Do NOT say "I didn't detect feedback." Proceed
directly to the Question Router.

### Error handling

All detection and capture logic MUST be wrapped in try/except. If file reads
or writes fail, skip capture entirely and proceed to routing. The analyst's
primary job is answering questions, not bookkeeping.

## Anti-Patterns

1. **Never block the pipeline** -- if capture fails, pass through silently
2. **Never ask the user to confirm feedback type** -- classify silently
3. **Never announce "no feedback detected"** -- pass through without comment
4. **Never do heavy processing** -- pattern match and write, nothing more
5. **Never overwrite existing corrections** -- always append
6. **Never fabricate correction details** -- use null for fields you cannot infer
