# Skill: History

## Purpose
Browse and search past analyses from the analysis archive. Helps users
recall what they've analyzed before, find prior findings, and build on
previous work.

## When to Use
- User says `/history` or "what have I analyzed before?"
- At session start, to provide context on prior work
- When framing a new question, to check if similar analysis exists

## Invocation
`/history` — list recent analyses (last 10)
`/history {id}` — show full details for a specific analysis
`/history search={term}` — search by title, question, or tags
`/history --all` — list all analyses across all datasets
`/history dataset={id}` — filter to a specific dataset

## Instructions

### Step 1: Load Archive
1. Read `.knowledge/analyses/index.yaml`
2. If empty: "No analyses archived yet. Complete an analysis and it will appear here."

### Step 2: Execute Command

**List recent (`/history`):**
- Filter to active dataset (unless `--all` flag)
- Sort by date descending
- Show last 10 as a table: date, title, level, key finding count, dataset
- Show total count: "Showing 10 of {total} analyses."

**Show specific (`/history {id}`):**
- Find entry by ID in index
- Display: title, date, question, level, all key findings, metrics used,
  agents used, output files, tags, confidence, recommendations
- If output files exist, offer: "Want to review the full analysis?"

**Search (`/history search={term}`):**
- Search across: title, question, key_findings, tags (case-insensitive)
- Display matching entries as a table
- If no matches: "No analyses match '{term}'. Try broader terms."

**All datasets (`/history --all`):**
- Include dataset_id column in output
- Sort by date descending across all datasets

### Step 3: Contextual Suggestions
After displaying history:
- "Want to re-run this analysis with fresh data?"
- "Want to build on finding #{n}?"
- If recent analysis was partial: "This analysis was incomplete. Resume with `/resume-pipeline`."

## Edge Cases
- **No active dataset:** Show all analyses or prompt to connect
- **Archive file missing:** Create empty index
- **Analysis output files deleted:** Note "output files no longer available"
- **Very long history (>100):** Paginate, show 20 at a time
