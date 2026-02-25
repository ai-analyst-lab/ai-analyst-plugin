# Skill: Stakeholder Communication Matrix

## Purpose
Adapt analytical findings to the audience — same insight, different framing, detail level, and format depending on who will read it. Ensures that executives get the bottom line, PMs get the implications, engineers get the specifics, and data teams get the methodology.

## When to Use
Apply this skill when producing a narrative (Storytelling agent), creating a deck (Deck Creator agent), or whenever the user specifies an audience. If no audience is specified, default to **Product Team** format.

## Instructions

### Pre-flight: Load Learnings
Before executing, check `.knowledge/learnings/index.md` for relevant entries:
- Read the file. If it doesn't exist or is empty, skip silently.
- Scan for entries under **"Communication"** and **"General"** headings (or related categories like "Stakeholder Preferences").
- If entries exist, incorporate them as constraints for this execution (e.g., audience-specific preferences, formatting conventions).
- Never block execution if learnings are unavailable.

### The Stakeholder Matrix

Different audiences care about different things. For the same finding, adapt:

| Dimension | Executive | Product Team | Engineering | Data Team |
|-----------|----------|-------------|-------------|-----------|
| **Lead with** | Business impact ($, users, risk) | What to do about it (action) | What's broken and where (specifics) | How we found it (methodology) |
| **Detail level** | Bottom line + 1 supporting fact | Findings + implications + next steps | Root cause + technical details + fix scope | Methodology + data quality + caveats |
| **Format** | 3 slides max / 1-paragraph summary | Analysis report with charts | Investigation log with queries/code | Full report with validation section |
| **Metrics language** | Revenue, users, growth rate | Conversion, retention, engagement | Error rate, latency, success rate | Statistical significance, confidence intervals |
| **Time horizon** | This quarter / this year | This sprint / this month | This release / this deploy | This analysis / this dataset |
| **Charts** | 1-2 high-level (big number, trend) | 3-5 focused (funnel, segmentation) | Technical plots (timelines, error logs) | Distribution, correlation, validation |
| **Caveats** | Only if they change the recommendation | Noted alongside findings | Noted with technical implications | Full methodology section |
| **Recommendation style** | "We should X" (decisive) | "I recommend X because Y" (reasoned) | "The fix is X, effort is Y" (scoped) | "The data supports X with caveats Y" (qualified) |

### How to Adapt

#### Step 1: Identify the Audience

If the user specifies an audience, use that. If not, ask or default to Product Team.

Common signals:
- "Prepare this for the leadership team" → Executive
- "What should we do about this?" → Product Team
- "Can you dig into the root cause?" → Engineering
- "How confident are we in this finding?" → Data Team

#### Step 2: Select the Lead

Every communication starts with the most important thing for that audience:

```
EXECUTIVE:    "This is costing us $X per month."
PRODUCT:      "Mobile checkout conversion dropped 15% — here's what to prioritize."
ENGINEERING:  "iOS app v2.3.0 has a payment processing regression in the checkout flow."
DATA:         "We isolated the root cause through 5 rounds of segment decomposition, controlling for seasonality."
```

Same finding. Different first sentence.

#### Step 3: Calibrate Detail

Use the pyramid principle — start with the conclusion, add detail as the audience requires:

```
Level 1 (Executive):     Conclusion + impact + recommendation
Level 2 (Product):       + key findings + implications + next steps
Level 3 (Engineering):   + root cause details + affected systems + fix scope
Level 4 (Data):          + methodology + validation + caveats + alternative explanations
```

Each level includes everything above it plus more depth.

#### Step 4: Adapt the Recommendation

| Audience | Recommendation Style | Example |
|----------|---------------------|---------|
| Executive | Decisive, resource-oriented | "Recommend allocating 2 engineers for 1 sprint to fix the iOS payment bug. Expected recovery: $64K/year." |
| Product | Reasoned, prioritized | "Recommend prioritizing the iOS payment fix over the checkout redesign. The bug affects 12% of transactions and has a clear fix, while the redesign has uncertain ROI." |
| Engineering | Specific, scoped | "The regression is in `PaymentProcessor.swift` introduced in v2.3.0 commit `abc123`. Hotfix path: revert the payment tokenization change and deploy v2.3.1." |
| Data | Qualified, methodical | "The data strongly supports a causal link between v2.3.0 and the ticket spike (r²=0.94, controlled for seasonality and mix shift). Recommend confirming with server logs before concluding." |

### Multi-Audience Documents

When a document serves multiple audiences (common for analysis reports):

1. **Start with Executive Summary** — 3-5 sentences, bottom line first
2. **Key Findings for Product** — what happened, why, what to do
3. **Technical Details for Engineering** — root cause, affected systems, fix scope
4. **Methodology for Data** — how the analysis was done, validation, caveats

Label sections clearly so readers can jump to their level.

### Output Format

When applying this skill, note the audience adaptation at the top of the deliverable:

```markdown
**Audience:** [Executive / Product / Engineering / Data / Multi-audience]
**Adapted for:** [Name or role, if known]
**Detail level:** [Level 1-4]
```

## Examples

### Example: Same Finding, Four Audiences

**Finding:** Support ticket volume spiked 55% in June due to an iOS payment bug in app v2.3.0, causing 356 excess tickets and ~$5,340 in support costs.

**Executive version:**
> Support costs increased $5,340/month due to an iOS app bug. Engineering has identified the fix. Recommend deploying the hotfix this sprint — expected to eliminate the excess ticket volume entirely.

**Product version:**
> iOS payment failures spiked in June after the v2.3.0 release, driving a 55% increase in support tickets. The bug affects checkout on iOS devices, causing payment processing errors that generate support contacts. Recommend prioritizing the hotfix (v2.3.1) over planned feature work this sprint. After the fix, monitor ticket volume for 2 weeks to confirm recovery.

**Engineering version:**
> The payment tokenization change in v2.3.0 (commit `abc123`, deployed Jun 1) introduced a regression in `PaymentProcessor.swift` that causes intermittent failures on iOS 16+ when using Apple Pay. The failure manifests as a timeout in the token exchange, which the client interprets as a generic error. 356 excess support tickets were generated between Jun 1-14. The fix is to revert the tokenization change and use the v2.2.x payment path until the token exchange timeout is resolved. Estimated effort: 2 story points.

**Data version:**
> We isolated the root cause through 5 rounds of iterative decomposition: total tickets → monthly anomaly (June) → category isolation (payment issues, 72% of excess) → device isolation (iOS, 89% of payment excess) → version isolation (v2.3.0, 95% of iOS excess). The finding is robust: segment-first checks showed no Simpson's Paradox, the anomaly period aligns precisely with the v2.3.0 release window (Jun 1-14), and the v2.4.0 hotfix on Jun 15 shows immediate recovery. Confidence: HIGH. Caveat: ticket categorization relies on agent tagging, which has ~8% misclassification rate for payment issues.

## Anti-Patterns

1. **Never give an executive a methodology-first report** — they need the bottom line, not how you got there
2. **Never give an engineer a business-impact-only summary** — they need the specifics to act on it
3. **Never skip the recommendation** — every audience needs to know what to do next, even if the framing differs
4. **Never assume one format fits all** — if you're presenting to a mixed group, use the multi-audience structure with labeled sections
5. **Never hide caveats from the data team** — they will find them and lose trust in the analysis
6. **Never overload executives with caveats** — mention only caveats that would change the recommendation
