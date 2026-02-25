# Skill: Analysis Design Spec

## Purpose
Ensure every analysis starts with a clear plan — what question it answers, what decision it informs, what data it needs, and what "done" looks like — before any queries are written or data is explored.

## When to Use
Apply this skill at the start of every new analysis, before running the Data Explorer or any analysis agent. If a user asks you to analyze something, produce an Analysis Design Spec first. Skip only if the user provides a request that already covers all seven fields (rare).

## Instructions

### The Analysis Design Spec

Before touching data, fill in this template. Every field is required. If you can't fill a field, ask the user.

```markdown
## Analysis Design Spec

### 1. Question
What are we trying to answer?
[A specific, testable question — apply the Question Framing skill]

### 2. Decision
What will this analysis inform?
[A concrete action the team will take based on the answer]
[If the answer is "nothing specific" — this may be reporting, not analysis. Confirm with the user.]

### 3. Data Needed
| Data | Source | Available? | Notes |
|------|--------|-----------|-------|
| [metric/field] | [table/system] | Yes/No/Partial | [gaps, quality concerns] |

### 4. Dimensions
What should we segment or decompose by?
- [Dimension 1]: [why — what would different values tell us?]
- [Dimension 2]: [why]
- [Dimension 3]: [why]

### 5. Time Range & Granularity
- **Period:** [start date — end date]
- **Granularity:** [daily / weekly / monthly]
- **Comparison:** [vs. prior period / vs. same period last year / vs. benchmark]

### 6. Output Format
What deliverable does the user need?
- [ ] Quick answer (1-2 sentences + supporting number)
- [ ] Analysis report (structured findings with charts)
- [ ] Presentation deck (slides for stakeholders)
- [ ] Data table (for further analysis by the user)

### 7. Success Criteria
How will we know the analysis answered the question?
[Specific conditions — e.g., "Identify which segment drove >50% of the decline"
or "Determine whether the change is statistically meaningful at the segment level"]
```

### How to Use the Spec

**Before analysis:**
1. Fill in all 7 fields
2. Confirm with the user if any field required assumptions
3. Flag any data gaps in field 3 (apply the Tracking Gaps skill if needed)
4. Use field 4 to inform which agents to invoke and what segmentation to run

**During analysis:**
- Check the spec before each major step — are you still answering the stated question?
- If the analysis reveals a more interesting question, note it but finish the original question first
- Use field 7 to know when to stop — avoid analysis rabbit holes

**After analysis:**
- Verify the deliverable matches field 6
- Verify the success criteria in field 7 are met
- If criteria aren't met, note what's missing and why

### Scope Calibration

Not every request needs the same depth. Use the question to calibrate:

| Request Type | Depth | Typical Agents | Time |
|-------------|-------|----------------|------|
| **Number pull** | "What was X last month?" | Data Explorer only | Minutes |
| **Monitoring** | "How is X trending?" | Overtime/Trend | 15-30 min |
| **Exploration** | "What's happening with X?" | Descriptive Analytics | 30-60 min |
| **Deep dive** | "Why did X change?" | Full pipeline including Root Cause Investigator | 1-2 hours |

Match the analysis depth to the question. A number pull doesn't need a full investigation pipeline.

### Writing Rules

1. **The question must be specific** — "How are users doing?" is not a question. "Did 7-day retention change for users who signed up after the redesign?" is.
2. **The decision must be actionable** — "We'll understand users better" is not a decision. "We'll decide whether to roll back the redesign" is.
3. **Dimensions must be justified** — don't segment by everything. Each dimension should have a reason: "Different devices have different UX, so conversion may differ."
4. **Success criteria must be falsifiable** — "Good analysis" is not a criterion. "Identify the segment responsible for >50% of the change" is.
5. **Output format must match the audience** — an executive gets a deck, a data scientist gets a table, a PM gets an analysis report.

## Examples

### Example 1: Root Cause Investigation

```markdown
## Analysis Design Spec

### 1. Question
Why did support ticket volume increase 55% in June compared to the prior 6-month average?

### 2. Decision
If the root cause is a product bug, we'll prioritize a hotfix. If it's seasonal or external, we'll adjust staffing.

### 3. Data Needed
| Data | Source | Available? | Notes |
|------|--------|-----------|-------|
| Support tickets (volume, category, severity) | {schema}.support_tickets | Yes | |
| User device and app version | {schema}.events | Yes | Need to join on user_id |
| Product release dates | Engineering team | Partial | May need to ask |

### 4. Dimensions
- Category: which types of tickets spiked?
- Device/platform: is it isolated to one platform?
- App version: did a specific release cause it?
- Severity: are these critical or minor?

### 5. Time Range & Granularity
- **Period:** Jan 1 – Jul 31 (7 months for baseline + anomaly)
- **Granularity:** Daily for the anomaly month, monthly for baseline
- **Comparison:** June vs. Jan-May average

### 6. Output Format
- [x] Analysis report (structured findings with charts)
- [ ] Presentation deck

### 7. Success Criteria
Identify the specific root cause (what changed, when, affecting whom) and quantify the excess ticket volume attributable to it.
```

### Example 2: Quick Number Pull

```markdown
## Analysis Design Spec

### 1. Question
What was the checkout conversion rate for mobile users last week?

### 2. Decision
Monitoring check — if it dropped below 2.5%, we'll investigate further.

### 3. Data Needed
| Data | Source | Available? | Notes |
|------|--------|-----------|-------|
| Checkout events by device | {schema}.events | Yes | |
| Purchase events | {schema}.orders | Yes | |

### 4. Dimensions
- None needed for the initial pull (just mobile, last week)

### 5. Time Range & Granularity
- **Period:** Last 7 days
- **Granularity:** Single number (weekly total)
- **Comparison:** vs. prior 4-week average

### 6. Output Format
- [x] Quick answer (1-2 sentences + supporting number)

### 7. Success Criteria
A single conversion rate number with context (vs. recent average). If below threshold, flag for investigation.
```

## Anti-Patterns

1. **Never start an analysis without knowing the decision it informs** — if you can't fill in field 2, you're doing a fishing expedition
2. **Never let the spec become a blocker** — for quick number pulls, fill it in one sentence per field and move on. The spec scales with the analysis complexity.
3. **Never ignore the spec mid-analysis** — if you discover something more interesting, note it as a follow-up question but finish what was asked first
4. **Never over-scope** — if the user asked a monitoring question, don't design a deep dive. Match the depth to the request.
5. **Never skip dimensions** — "Let me segment by everything" is not a plan. Choose 2-4 dimensions with reasons.
