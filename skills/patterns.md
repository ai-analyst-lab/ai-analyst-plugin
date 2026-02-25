# Skill: Patterns

## Purpose
Browse and search recurring patterns discovered across analyses. Patterns
are auto-extracted after each analysis archive and represent behaviors that
appear consistently in the data.

## When to Use
- User says `/patterns` or "what patterns have we seen?"
- During analysis, to check if a finding matches a known pattern
- At session start, to remind the user of established behaviors

## Invocation
`/patterns` — list patterns for the active dataset
`/patterns --global` — list patterns across all datasets
`/patterns search={term}` — search patterns by keyword
`/patterns {id}` — show full details for a specific pattern

## Instructions

### Step 1: Load Patterns
1. Read `.knowledge/analyses/_patterns.yaml` for the active dataset.
2. If `--global` flag: also read `.knowledge/global/cross_dataset_observations.yaml`.
3. If empty: "No patterns recorded yet. Complete a few analyses and patterns will emerge."

### Step 2: Execute Command

**List patterns (`/patterns`):**
- Filter to active dataset (unless `--global`)
- Sort by occurrences descending (most established first)
- Display as a table: type, description, occurrences, confidence, last seen
- Show total count

**Show specific (`/patterns {id}`):**
- Display: description, type, all evidence (with analysis IDs), dimensions,
  metrics, suggested investigation
- Offer: "Want to investigate this pattern further?"

**Search (`/patterns search={term}`):**
- Search across description, dimensions, metrics, tags
- Display matching patterns as a table

**Global (`/patterns --global`):**
- Include cross-dataset observations alongside per-dataset patterns
- Note which dataset each pattern was observed in

### Step 3: Contextual Suggestions
After displaying patterns:
- "Want to check if {pattern} still holds in the current data?"
- "Want to use {pattern} as context for a new analysis?"
- "This pattern was last seen {N} days ago — may need revalidation."

## Pattern Extraction (Auto)

After each analysis archive (triggered by archive-analysis skill), scan the
new analysis for potential patterns:

1. Compare new findings to existing patterns:
   - If a finding matches an existing pattern → increment occurrences, update last_seen
   - If a finding is new but could extend a pattern → add as evidence
2. Look for NEW patterns:
   - Same metric behavior across 2+ analyses → candidate pattern
   - Same segment consistently outperforming → candidate pattern
   - Recurring anomaly at similar times → candidate pattern
3. Write updated patterns back to `_patterns.yaml`

Minimum 2 occurrences to create a pattern. Single-occurrence findings are
just findings, not patterns.

## Edge Cases
- **No patterns:** Suggest running more analyses
- **Stale patterns (last_seen >60 days):** Flag as potentially outdated
- **Contradictory patterns:** Flag and suggest investigation
- **Too many patterns (>50):** Show top 20 by occurrences, offer pagination
