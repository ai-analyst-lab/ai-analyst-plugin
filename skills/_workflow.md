# Workflow: Agents and Default Pipeline

## Your Agents

**How agents work in this system:** Agents are markdown prompt templates. Claude reads the file, substitutes `{{VARIABLES}}`, and follows instructions step by step. Agents run sequentially (single-thread), sharing conversation context. Working files in `working/` and `outputs/` preserve state. Use `/resume-pipeline` if context gets long.

To run an agent:
1. Read the agent file
2. Substitute the `{{VARIABLES}}` with actual values from the current context
3. Execute the workflow step by step

See `agents/INDEX.md` for the complete list of agents, system variables, and when to invoke each agent.

**Skills vs. agents:** Skills are always active -- they shape everything you do.
Agents are invoked on demand for specific tasks. Skills define HOW to do things
well. Agents DO multi-step work.

---

## Default Workflow

When asked to analyze data, follow this process:

1. **Frame the question** -- What decision will this inform? What do we expect
   to find? (Use Question Framing skill or agent)
2. **Design the analysis** -- Confirm question, decision, data needed, dimensions,
   output format, and success criteria before touching data.
   (Use Analysis Design Spec skill)
3. **Form hypotheses** -- Generate testable hypotheses across multiple cause
   categories: Product Changes, Technical Issues, External Factors, Mix Shift.
   (Use Hypothesis agent)
4. **Explore the data** -- What is in this dataset? What is the quality? Any
   gaps? (Use Data Explorer agent + Data Quality Check skill)
4.5. **Source tie-out** -- Verify data loaded correctly by comparing pandas
   direct-read vs DuckDB SQL on foundational metrics (row counts, nulls,
   numeric sums). HALT if any mismatch. (Use Source Tie-Out agent)
5. **Analyze** -- Segment, funnel, decompose, trend -- whatever the question
   requires. Always run the segment-first Simpson's Paradox check before
   concluding. (Use Descriptive Analytics or Overtime/Trend agent)
6. **Investigate root cause** -- If analysis found an anomaly or unexpected
   pattern, drill down iteratively through dimensions until reaching a specific,
   actionable root cause. (Use Root Cause Investigator agent)
7. **Validate** -- Check your SQL. Verify the numbers add up. Cross-reference.
   Check guardrail metrics for any positive findings.
   (Use Validation agent + Triangulation skill + Guardrails Awareness skill)
8. **Size the opportunity** -- If the analysis recommends an investment or fix,
   quantify the business impact with sensitivity analysis.
   (Use Opportunity Sizer agent)
9. **Design the storyboard** -- Build narrative beats (Context-Tension-Resolution)
   from findings, then map each beat to a visual format. Pass {{CONTEXT}} if
   the output is a workshop or talk (adds Closing beats for CTA sequence).
   (Use Story Architect agent)
10. **Review storyboard coherence** -- Verify the storyboard tells a coherent
    story with no gaps BEFORE any charting work begins. Validates Closing beats
    if present. (Use Narrative Coherence Reviewer agent)
11. **Fix storyboard** -- If NEEDS ADDITIONS or NEEDS RESEQUENCING, revise the
    storyboard beats. (Story Architect revises)
12. **Generate charts** -- Create each chart from the storyboard. For each beat,
    traverse the `slides` array and generate charts for slides with
    `type: chart-full` (or `chart-left`/`chart-right`).
    (Use Chart Maker agent, once per chart spec)
13. **Review chart design** -- Check every chart against the SWD checklist.
    (Use Visual Design Critic agent -- chart-level review)
14. **Fix charts** -- The DAG engine automatically runs `chart-maker-fixes`
    when the design critic returns APPROVED WITH FIXES (passes the fix report
    as `FIX_REPORT` input). If NEEDS REVISION, the pipeline HALTs for manual
    intervention — return to step 9 to revise the storyboard.
15. **Tell the story** -- Write the narrative using the storyboard as structure.
    (Use Storytelling agent + Stakeholder Communication skill)
16. **Create the deck** -- Build the slide deck from narrative + charts. Deck
    Creator auto-selects theme based on context: workshop/talk defaults to
    analytics-dark, all other contexts default to analytics (light). Pass
    {{THEME}} to override. (Use Deck Creator agent)
17. **Review deck design** -- Check the Marp deck for font sizes, theme
    consistency, and dark mode rendering issues. Pass {{DECK_FILE}} and
    {{THEME}}. (Use Visual Design Critic agent -- slide-level review)
18. **Close the loop** -- Ensure every recommendation has a decision owner,
    success metric, follow-up date, and fallback plan.
    (Use Close-the-Loop skill)
19. **Draft communications** -- Generate stakeholder-ready communications
    (Slack summary, email brief, exec summary). Non-critical — pipeline
    continues if this fails.
    (Use Comms Drafter agent + Stakeholder Communication skill)

You can skip steps when they do not apply. If the user just wants a chart, go
straight to Chart Maker. If they want to validate existing work, go straight
to Validation. Use judgment.

**Quick Answer Path (L1/L2):** For simple factual lookups ("How many users?")
or basic comparisons ("Revenue by category"), skip the full pipeline. Query
the data directly, apply chart style if visual output is needed, cite the
source, and return the answer. No agents required. Use the Question Router
skill to classify — L1/L2 questions should be answered in under 2 minutes.

Always start with step 1 (framing) unless the user has already framed the
question clearly or the Question Router classifies the request as L1/L2.
