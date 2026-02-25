# Skill: Triangulation / Sanity Check

## Purpose
Cross-reference analytical findings against multiple data sources, external benchmarks, and common sense to catch errors before they become bad decisions.

## When to Use
Apply this skill after every analysis, before presenting findings to stakeholders, and whenever a result seems surprising. If a finding would change a decision, it MUST be triangulated first.

## Instructions

### Triangulation Framework

Every finding gets checked through four lenses — starting with the most common source of misleading results:

```
CHECK 0: SEGMENT-FIRST  → Does this hold at the segment level, or is it a Simpson's Paradox?
CHECK 1: INTERNAL        → Do the numbers add up within the analysis?
CHECK 2: CROSS-REFERENCE → Does another data source agree?
CHECK 3: PLAUSIBILITY    → Does this make sense given what we know about the world?
```

### Check 0: Segment-First (Mandatory)

**Run this check BEFORE accepting any aggregate finding.** Simpson's Paradox is the #1 source of misleading analytical conclusions — an aggregate trend that reverses when you look at segments.

**Default segments to always check** (use whichever are available in the data):
1. Platform / device (mobile vs. desktop vs. tablet)
2. User type / plan tier (free vs. paid, plan levels)
3. Geography / region (US vs. EU vs. APAC)
4. Acquisition channel (organic vs. paid vs. referral)

**Process for each aggregate finding:**
1. Compute the finding metric for the aggregate (all users/records)
2. Compute the same metric for each value of at least 2 default segment dimensions
3. Check: does ANY segment show a trend **opposite** to the aggregate?

**If opposite trends detected:**
```
⚠️ SIMPSON'S PARADOX DETECTED

The aggregate [metric] shows [aggregate trend].
However, [segment value] shows the OPPOSITE: [segment trend].

The aggregate is misleading because [explanation — e.g., the growing
segment masks the declining segment].

Action: Report segment-level findings instead of aggregate. Flag this
prominently in the Executive Summary.
```

**If no opposite trends detected:**
Record: "Segment-first check PASSED — aggregate trends are consistent with [dimensions checked] segment-level trends."

**Include in the Validation Report:**
```markdown
| Check | Result | Detail |
|-------|--------|--------|
| Segment-first (platform) | PASS/FAIL | [specifics] |
| Segment-first (user type) | PASS/FAIL | [specifics] |
```

This check typically takes 2-3 queries and prevents the most common analytical error. Never skip it.

### Check 1: Internal Consistency

**Arithmetic checks:**
- Do percentages sum to 100% (±1% for rounding)?
- Does the sum of segments equal the total?
- Do period-over-period changes recalculate correctly?
- Is revenue = price × quantity × (1 - discount)?

**Logical checks:**
- Is the funnel monotonically decreasing? (more visitors than signups than purchases)
- Are rates between 0% and 100%?
- Are dates in chronological order?
- Is the denominator stable, or did it change? (a "drop" in conversion might be a spike in traffic)

```python
def check_internal_consistency(findings):
    checks = []
    for finding in findings:
        # Segment sum check
        if finding.has_segments:
            segment_sum = sum(finding.segment_values)
            total = finding.total_value
            if abs(segment_sum - total) / total > 0.02:
                checks.append(("FAIL", f"Segments sum to {segment_sum}, but total is {total}"))

        # Rate bounds check
        if finding.is_rate:
            if finding.value < 0 or finding.value > 1:
                checks.append(("FAIL", f"{finding.name} = {finding.value} is outside [0,1]"))

        # Funnel monotonicity
        if finding.is_funnel:
            for i in range(1, len(finding.steps)):
                if finding.steps[i] > finding.steps[i-1]:
                    checks.append(("FAIL", f"Funnel step {i} ({finding.steps[i]}) > step {i-1} ({finding.steps[i-1]})"))
    return checks
```

### Check 2: Cross-Reference

**Calculate the same thing two different ways:**
- Revenue from orders table vs. revenue from payments table
- User count from events table vs. user count from users table
- Conversion rate from funnel query vs. conversion rate from separate numerator/denominator queries

**Compare against related metrics:**
- If conversion rate went up, did absolute conversions also go up? (denominator check)
- If revenue grew, did order count or average order value grow? (which component?)
- If churn increased, did new user signups decrease? (is it a cohort effect?)

**Time-based cross-reference:**
- Does the daily data sum to the weekly data?
- Does the weekly data sum to the monthly data?
- Are there timezone-related discrepancies?

### Check 3: External Plausibility

**Order-of-magnitude checks for common metrics:**

| Metric | Typical Range | If Outside Range |
|--------|--------------|------------------|
| SaaS conversion (free → paid) | 2-5% | >10% suspicious; <1% possible but check |
| E-commerce conversion | 1-4% | >8% check for bot filtering issues |
| Email open rate | 15-30% | >50% check for pixel tracking issues |
| Click-through rate (email) | 2-5% | >15% suspicious |
| Monthly churn (SaaS) | 3-8% | <1% check for measurement window; >15% check definition |
| DAU/MAU ratio | 10-25% (B2B SaaS) | >40% unusual for non-social products |
| NPS | 20-50 (good SaaS) | >70 or <-10 check sample methodology |
| Mobile share of traffic | 50-70% (consumer) | <30% check if app traffic is included |
| Bounce rate | 40-60% | <20% check for double-firing analytics |
| Average session duration | 2-5 min (consumer) | >15 min check for session timeout definition |

**Benchmark sources:**
- Mixpanel Product Benchmarks Report (annual, free)
- Lenny Rachitsky's benchmarks (newsletter, SaaS-focused)
- First Round's State of Startups (annual survey)
- Recurly churn benchmarks (subscription businesses)
- Statista (general industry benchmarks)
- SimilarWeb (traffic benchmarks)

### Common Analytical Errors to Check

#### Simpson's Paradox
**What it is:** A trend that appears in several groups reverses when the groups are combined.
**How to check:** Always look at both the aggregate AND the segmented view. If they disagree, investigate the segment sizes.
**Example:** Overall conversion went up, but conversion went DOWN in every segment. Cause: the highest-converting segment grew as a share of traffic.

#### Survivorship Bias
**What it is:** Analyzing only the data that "survived" a selection process, ignoring what was filtered out.
**How to check:** Ask "what's NOT in this dataset?" Check if churned users, failed transactions, or deleted accounts are excluded.
**Example:** "Average revenue per user increased!" — but only because low-spending users churned, leaving only high-spenders.

#### Time Zone Issues
**What it is:** Events counted in different time zones create artificial spikes or dips at day boundaries.
**How to check:** Look at hourly distributions. If there's a spike at midnight UTC, check if events are being bucketed incorrectly.
**Example:** "Signups spike at midnight" — because the mobile app reports in local time but the backend stores in UTC.

#### Incomplete Data Windows
**What it is:** Comparing periods where one period has incomplete data (e.g., comparing full January to partial February).
**How to check:** Always verify the data range is complete. Check the latest event date. Compare like-for-like periods.
**Example:** "February revenue dropped 40%!" — but it's February 15th, and you're comparing to all of January.

#### Denominator Changes
**What it is:** A rate changes not because the behavior changed, but because the pool being measured changed.
**How to check:** Always look at numerator and denominator separately before interpreting the ratio.
**Example:** "Conversion rate doubled!" — because a marketing campaign brought in low-intent traffic (denominator spiked, numerator stayed flat, then the campaign ended and denominator dropped back).

#### Correlation ≠ Causation
**What it is:** Two metrics move together, but one doesn't cause the other.
**How to check:** Look for confounders. Ask "what else changed at the same time?" Check if the relationship holds across different segments.
**Example:** "Users who use Feature X have 2x retention" — but maybe power users both use Feature X AND have high retention because they're power users, not because Feature X causes retention.

### Output Format: Validation Report

```markdown
# Validation Report: [Analysis Name]
## Date: [YYYY-MM-DD]

### Overall Confidence: [HIGH / MEDIUM / LOW]

### Finding-by-Finding Validation

#### Finding 1: [statement]
| Check | Result | Detail |
|-------|--------|--------|
| Internal consistency | PASS/WARN/FAIL | [specifics] |
| Cross-reference | PASS/WARN/FAIL | [specifics] |
| External plausibility | PASS/WARN/FAIL | [specifics] |
| Analytical errors | PASS/WARN/FAIL | [which errors checked, any found] |
| **Confidence** | **HIGH/MEDIUM/LOW** | [summary justification] |

[Repeat for each finding]

### Caveats for Stakeholders
[What should be mentioned when presenting these findings]

### Recommended Additional Validation
[What would increase confidence — more data, different analysis, A/B test]
```

## Examples

### Example 1: Catching a Denominator Change
**Finding:** "Mobile conversion rate increased from 2.1% to 3.4% in March"
**Cross-reference check:** Look at numerator and denominator separately.
- Mobile purchases: 1,050 → 1,020 (actually DOWN slightly)
- Mobile visitors: 50,000 → 30,000 (DOWN significantly — a paid campaign ended)
**Verdict:** WARN — Conversion rate "improved" only because low-intent paid traffic disappeared. Actual purchases decreased. The finding is technically true but deeply misleading.

### Example 2: Catching Simpson's Paradox
**Finding:** "Overall activation rate improved from 45% to 48% this quarter"
**Segment check:**
- Enterprise: 62% → 58% (down)
- SMB: 41% → 38% (down)
- Free tier: 32% → 29% (down)
**But:** Enterprise share of signups grew from 15% to 35%.
**Verdict:** FAIL — Every segment got worse. The "improvement" is entirely due to mix shift toward higher-activating enterprise segment. The actual product experience degraded.

### Example 3: Plausibility Catch
**Finding:** "Email campaign achieved 72% open rate"
**External plausibility:** Industry average is 15-30%. 72% is extreme.
**Investigation:** Apple Mail Privacy Protection pre-fetches email images, inflating open rates for Apple Mail users. 68% of the list uses Apple Mail.
**Verdict:** WARN — True open rate is likely 25-35% after adjusting for Apple privacy pre-fetching. Report adjusted number alongside raw number.

## Anti-Patterns

1. **Never present a surprising finding without triangulating it** — if it's surprising, it's either a breakthrough or an error. Check which one.
2. **Never skip the denominator check** — more analytical errors come from denominator changes than any other cause
3. **Never rely on a single data source** — if the finding matters, verify it from a different angle
4. **Never ignore external benchmarks** — if your metric is 10x the industry average, that's a red flag, not a celebration
5. **Never say "the data shows" without saying "we checked by..."** — triangulation is what separates analysis from data regurgitation
6. **Never treat WARN findings as PASS** — a warning means the finding needs a caveat when presented to stakeholders
