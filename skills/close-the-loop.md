# Skill: Close-the-Loop

## Purpose
Ensure every analysis that includes a recommendation ends with a clear follow-up plan — who decides, what metric tracks success, when to check back, and what to do if the expected outcome doesn't materialize.

## When to Use
Apply this skill at the end of any analysis that produces a recommendation or action item. If the analysis concludes with "we should do X," this skill ensures X actually gets tracked and evaluated. Skip only for pure exploratory analyses with no recommendation.

## Instructions

### The Close-the-Loop Checklist

Append this checklist to the end of every analysis report or presentation that includes a recommendation:

```markdown
## Close the Loop

### Decision
- **Recommendation:** [What the analysis recommends]
- **Decision maker:** [Who will approve/reject this — name or role]
- **Decision deadline:** [When this needs to be decided by]
- **Decision made:** [ ] Yes / [ ] No / [ ] Deferred
- **Decision outcome:** [What was actually decided — fill in after]

### Success Tracking
- **Success metric:** [What metric will tell us the recommendation worked?]
- **Current baseline:** [What is the metric today?]
- **Target:** [What value do we expect if the recommendation works?]
- **Measurement window:** [How long after implementation before we evaluate?]
- **Data source:** [Where to pull the metric]

### Follow-Up
- **Check-in date:** [When to evaluate whether the recommendation worked]
- **Owner:** [Who is responsible for the follow-up check]
- **If successful:** [What's the next step — scale it, document it, move to next priority]
- **If unsuccessful:** [What's the fallback — investigate further, try alternative, accept the status quo]
- **If inconclusive:** [What additional data or time is needed before deciding]

### Analysis Provenance
- **Analysis date:** [When this analysis was completed]
- **Analyst:** [Who produced it]
- **Key assumptions:** [1-3 assumptions the recommendation depends on]
- **Confidence level:** [HIGH / MEDIUM / LOW]
- **What would change the recommendation:** [Under what conditions should we revisit]
```

### Why Each Field Matters

| Field | Why It Matters |
|-------|---------------|
| **Decision maker** | Without an owner, recommendations float. Someone must say yes or no. |
| **Decision deadline** | Without a deadline, the decision gets deferred indefinitely. Most analytical insights have a shelf life. |
| **Success metric** | Without a success metric, you can't tell if the recommendation worked. |
| **Current baseline** | Without a baseline, you can't measure improvement. "Conversion improved" means nothing without "from what?" |
| **Target** | Without a target, any change looks like success. Set a bar. |
| **Measurement window** | Some changes take weeks to show results. Define when to check. |
| **Check-in date** | The follow-up is the most commonly skipped step. Set a date. |
| **If unsuccessful** | Pre-commit to the fallback so you don't rationalize a failed recommendation after the fact. |

### Filling in the Checklist

**What you can fill in (as the analyst):**
- Recommendation (from the analysis)
- Success metric, baseline, and target (from the data)
- Measurement window (based on typical lag for this metric)
- Key assumptions and confidence level (from the analysis)
- What would change the recommendation (from sensitivity analysis, if available)

**What the user must fill in (prompt them):**
- Decision maker
- Decision deadline
- Owner for follow-up
- Check-in date

When the user must fill in fields, prompt them explicitly:

> This analysis recommends [X]. To close the loop, I need to know:
> 1. Who will decide whether to proceed? (decision maker)
> 2. By when does this need to be decided? (deadline)
> 3. Who will check whether it worked? (follow-up owner)

### Connecting to Opportunity Sizing

If the analysis used the Opportunity Sizer agent, connect the success tracking to the sizing model:

```markdown
### Success Tracking (from Opportunity Sizing)
- **Success metric:** [same as the primary metric in the sizing model]
- **Current baseline:** [from the base case computation]
- **Target (base case):** [from the base case impact]
- **Target (pessimistic):** [from the pessimistic scenario]
- **Break-even threshold:** [from the break-even analysis — "if improvement < X%, not worth it"]
- **Measurement window:** [long enough to observe the expected impact]
```

This directly links the "was it worth it?" question to the sizing model's assumptions.

## Examples

### Example 1: Bug Fix Recommendation

```markdown
## Close the Loop

### Decision
- **Recommendation:** Deploy hotfix v2.3.1 to resolve iOS payment processing regression
- **Decision maker:** Engineering lead (Priya)
- **Decision deadline:** End of this sprint (Feb 21)
- **Decision made:** [ ] Yes / [ ] No / [ ] Deferred
- **Decision outcome:** _[pending]_

### Success Tracking
- **Success metric:** Weekly support ticket volume (payment category, iOS)
- **Current baseline:** 89 tickets/week (anomaly period average)
- **Target:** <40 tickets/week (pre-anomaly baseline)
- **Measurement window:** 2 weeks after hotfix deploy
- **Data source:** {schema}.support_tickets, filtered to category='payment' AND device='iOS'

### Follow-Up
- **Check-in date:** 2 weeks after deploy
- **Owner:** _[to be assigned]_
- **If successful:** Document the incident, update monitoring to catch similar regressions earlier
- **If unsuccessful:** Investigate whether the root cause is actually v2.3.0 or a deeper issue; escalate to senior engineering
- **If inconclusive:** Extend measurement window to 4 weeks; check for confounding events

### Analysis Provenance
- **Analysis date:** 2026-02-14
- **Analyst:** AI Product Analyst
- **Key assumptions:** (1) The v2.3.0 release is the sole cause of the ticket spike, (2) The hotfix fully resolves the payment processing issue, (3) No other changes affect payment tickets during the measurement window
- **Confidence level:** HIGH
- **What would change the recommendation:** If the v2.3.0 → ticket spike correlation breaks down when controlling for a third variable, or if the hotfix was already deployed and tickets didn't recover
```

### Example 2: Strategic Recommendation

```markdown
## Close the Loop

### Decision
- **Recommendation:** Invest in mobile checkout optimization (projected $480K annual revenue impact)
- **Decision maker:** VP Product
- **Decision deadline:** Q2 planning (Mar 15)
- **Decision made:** [ ] Yes / [ ] No / [ ] Deferred
- **Decision outcome:** _[pending]_

### Success Tracking
- **Success metric:** Mobile checkout conversion rate
- **Current baseline:** 2.1%
- **Target (base case):** 3.4% (+62%)
- **Target (pessimistic):** 2.7% (+29%)
- **Break-even threshold:** 2.3% (+10%) — below this, the investment ROI is negative
- **Measurement window:** 8 weeks after changes ship (4 weeks ramp + 4 weeks measurement)
- **Data source:** {schema}.events (checkout_viewed → purchase_completed, device='mobile')

### Follow-Up
- **Check-in date:** 8 weeks after ship
- **Owner:** _[to be assigned]_
- **If successful:** Expand optimization to tablet; investigate next-largest conversion bottleneck
- **If unsuccessful:** Conduct user research on mobile checkout friction; consider A/B testing specific elements
- **If inconclusive:** Extend to 12 weeks; segment by device model and OS version for more signal

### Analysis Provenance
- **Analysis date:** 2026-02-14
- **Analyst:** AI Product Analyst
- **Key assumptions:** (1) Mobile conversion gap is due to UX friction, not user intent differences, (2) 30% of the gap is closeable through checkout optimization, (3) $47 AOV remains stable
- **Confidence level:** MEDIUM
- **What would change the recommendation:** If mobile users have fundamentally different purchase intent (not just friction), or if the AOV for mobile is significantly lower than desktop, the revenue projection would change
```

## Anti-Patterns

1. **Never end an analysis with just a recommendation** — a recommendation without follow-up tracking is a suggestion that gets forgotten
2. **Never skip the baseline** — "improve conversion" is meaningless without "from 2.1%"
3. **Never set a target without a measurement window** — conversion could improve in 2 days or 2 months; define when to check
4. **Never leave the decision maker blank** — if no one owns the decision, no one makes it
5. **Never skip the "if unsuccessful" plan** — pre-committing to a fallback prevents sunk-cost rationalization
6. **Never set the check-in date too far out** — if the measurement window is 2 weeks, the check-in should be 2-3 weeks after ship, not 6 months later
