# Skill: Question Router

## Purpose
Classify incoming user questions into complexity levels (L1-L5) and route
them to the appropriate response path. This replaces the old "skip-step"
logic with a structured classification that adapts the workflow depth to
the question's actual needs.

## When to Use
- At the start of every user interaction that looks like an analytical request
- Before launching the full 18-step pipeline
- When the user asks a follow-up question mid-analysis

## Classification Levels

### L1: Factual Lookup
**Pattern:** User wants a specific number or fact from the data.
**Examples:**
- "How many users signed up in March?"
- "What's the average order value?"
- "How many products are in the electronics category?"

**Response path:** Query the data directly. Return the answer with source
citation (table, column, filter). No agents needed.

**Time:** ~30 seconds

### L2: Simple Comparison
**Pattern:** User wants to compare two things or see a breakdown.
**Examples:**
- "Compare conversion rates by device"
- "Show me revenue by category"
- "What's the split of users by acquisition channel?"

**Response path:** Query + quick chart. Use `chart_helpers` directly.
Apply Visualization Patterns skill. No full pipeline.

**Time:** ~2 minutes

### L3: Guided Analysis
**Pattern:** User has a specific analytical question requiring multiple steps.
**Examples:**
- "Why did conversion drop last month?"
- "Which user segment has the highest LTV?"
- "Is our new checkout flow performing better?"

**Response path:** Subset of the pipeline — Frame → Explore → Analyze →
Validate → Present findings. Skip storyboard/deck unless requested.
Use 3-5 agents.

**Time:** ~10 minutes

### L4: Deep Investigation
**Pattern:** User needs root cause analysis, opportunity sizing, or
experiment design.
**Examples:**
- "Investigate why mobile revenue dropped 15% in Q3"
- "Size the opportunity if we fix the cart abandonment issue"
- "Design an A/B test for the new pricing page"

**Response path:** Full pipeline minus deck. Frame → Hypothesize → Explore →
Analyze → Root Cause → Validate → Size → Present findings.
Use 6-10 agents.

**Time:** ~20 minutes

### L5: Full Presentation
**Pattern:** User wants a complete analysis with a polished slide deck.
**Examples:**
- "Run the full pipeline on Q4 performance"
- `/run-pipeline`
- "Build me a board-ready deck on our retention problem"

**Response path:** Complete 18-step pipeline. All agents, full storyboard,
charts, narrative, and Marp deck.

**Time:** ~30-45 minutes

## Classification Algorithm

### Step 0: Pre-flight (runs on every query before classification)

Enrichment steps — never block routing. If any sub-step fails, skip it silently.

1. **Feedback check** — The Feedback Capture skill runs BEFORE this router.
   By the time a message reaches here, corrections/learnings are already
   captured. If the message was purely feedback (no analytical question),
   it was handled upstream — skip routing.

2. **Entity disambiguation** — If the entity index is loaded (from bootstrap):
   - Call `resolve_entity(query_text, entity_index)` from
     `helpers/entity_resolver.py`.
   - If matches found, call `format_disambiguation(matches)` and set
     `{{RESOLVED_ENTITIES}}` for downstream agents.
   - Example: "why is cvr dropping?" → Resolved: 'cvr' -> conversion_rate (metric)
   - If entity index unavailable or no matches, leave `{{RESOLVED_ENTITIES}}` empty.

3. **Corrections check** — Read `.knowledge/corrections/index.yaml`.
   - If `total_corrections > 0` for the active dataset, set
     `{{CORRECTION_COUNT}}` so analysis agents check the correction log
     before writing SQL (e.g., known join pitfalls, filter requirements).
   - If index is missing or `total_corrections` is 0, set
     `{{CORRECTION_COUNT}}` to 0.

4. **Archaeology note** — The Query Archaeology skill provides SQL pattern
   context (prior queries, reusable CTEs) to analysis agents when available.
   No action needed here — just acknowledge it flows downstream automatically.

After pre-flight completes, proceed to Step 1.

### Step 1: Parse the question

Extract:
- **Subject:** What entity/metric is being asked about?
- **Action:** Lookup, compare, analyze, investigate, or present?
- **Scope:** Single metric, breakdown, multi-dimensional, or end-to-end?
- **Output expectation:** Number, chart, findings, or deck?

### Step 2: Score complexity signals

| Signal | L1 | L2 | L3 | L4 | L5 |
|--------|----|----|----|----|-----|
| Asks for a single number | +3 | | | | |
| Uses "compare" or "by {dimension}" | | +3 | | | |
| Uses "why", "investigate", "root cause" | | | | +3 | |
| Uses "analyze", "what's happening with" | | | +3 | | |
| Mentions "deck", "presentation", "slides" | | | | | +3 |
| Uses `/run-pipeline` | | | | | +5 |
| Mentions sizing, opportunity, impact | | | | +2 | |
| Mentions experiment, A/B test | | | | +2 | |
| Question has multiple sub-questions | | | +2 | +1 | |
| "Quick" or "just" qualifier | +2 | +1 | | | |

Assign the level with the highest score. Ties break toward the lower level
(prefer faster response).

### Step 3: Adapt from user profile

If `.knowledge/user/profile.md` exists, read the user's preferences:
- **Detail level = "executive-summary":** Bias one level down (L3 → L2)
- **Detail level = "deep-dive":** Bias one level up (L2 → L3)
- **Technical level = "advanced":** Show more SQL, skip explanations
- **Technical level = "beginner":** Add more context, explain terms

### Step 4: Confirm with the user (for L3+)

For L1-L2: Execute immediately. No confirmation needed.

For L3-L5: Brief the user on the plan:
```
I'd classify this as a **[Level] — [Label]**. Here's my plan:
1. [Step summary]
2. [Step summary]
...
Estimated time: ~[X] minutes. Want me to proceed, or adjust the scope?
```

The user can:
- **Confirm:** Proceed with the plan
- **Adjust up:** "Go deeper" → bump to next level
- **Adjust down:** "Just give me the quick answer" → drop to lower level

## Integration with Pipeline

When routed to L3+, the Question Router hands off to the appropriate agents
by setting the entry point in the Default Workflow:

| Level | Entry Point | Exit Point |
|-------|-------------|------------|
| L3 | Step 1 (Frame) | Step 7 (Validate) — present findings inline |
| L4 | Step 1 (Frame) | Step 8 (Size) — present findings inline |
| L5 | Step 1 (Frame) | Step 18 (Close the Loop) — full deck |

## Dataset Detection

Before classifying, check whether the question references a dataset other than
the currently active one.

### Scan for dataset references

1. Read `.knowledge/datasets/` to get all known dataset IDs and display names.
2. Scan the user's question for exact or fuzzy matches to any dataset name.
3. If a non-active dataset is referenced:
   - Inform the user: "It looks like you're asking about **{display_name}**, but
     the active dataset is **{active_display_name}**."
   - Offer: "Want me to switch? (`/switch-dataset {id}`)"
   - Do NOT proceed with analysis until the user confirms which dataset to use.
4. If no dataset reference is found, proceed with the active dataset.

This prevents accidentally running analysis on the wrong dataset.

## Contextual Suggestions

After delivering results at any level, offer 2-3 relevant next actions based
on what was just completed. Match suggestions to the level and findings.

**After L1/L2 results:**
- "Want to break this down by [dimension from schema]?"
- "Want to see how this trended over time?"
- "Want to compare this across [available segment]?"

**After L3 findings:**
- "Want me to investigate the root cause of [top finding]?"
- "Want to size the opportunity if we fix [issue]?"
- "Want a deck of these findings for [audience]?"

**After L4 investigation:**
- "Want me to design an experiment to test [hypothesis]?"
- "Want a presentation-ready deck?"
- "Want to check this against [related metric from dictionary]?"

**After L5 deck delivery:**
- "Want to archive this analysis? (`/archive`)"
- "Want to explore a related question?"
- "Want to export in a different format? (`/export`)"

Always tailor suggestions to the actual findings — reference specific metrics,
segments, or anomalies discovered. Generic suggestions ("want to know more?")
are not helpful.

## Edge Cases

- **Ambiguous questions:** Default to L2, ask a clarifying question. "Do you
  want a quick breakdown, or should I investigate the drivers?"
- **Follow-up after analysis:** Re-classify. "Now make a deck" bumps a
  completed L3 to L5 (but reuses existing analysis, skips to Step 9).
- **Multiple questions in one message:** Classify each separately. Execute
  the highest-level one, note the others as follow-ups.
- **Non-analytical requests:** "Help me write a SQL query" or "Explain this
  chart" — handle directly without classification.

## Anti-Patterns

1. **Never run the full 18-step pipeline for an L1 question.** "How many
   users do we have?" should not trigger hypothesis generation.
2. **Never skip validation for L3+ questions.** Even guided analyses need
   a sanity check before presenting results.
3. **Never assume the user wants a deck.** Only create slides if explicitly
   requested or classified as L5.
4. **Never re-classify mid-execution without user input.** If you realize
   the question is more complex than initially classified, pause and ask.
