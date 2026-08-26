---
name: drop-off-format
description: >-
  Every step-to-step drop-off must show three numbers: raw users entering the step, raw users
  exiting, and the drop-off percentage. Trigger whenever output contains funnel steps, conversion
  rates between stages, or step-to-step comparisons, in tables, narrative, chart annotations, or
  Slack posts. A drop-off shown as only a raw count or only a percentage is incomplete.
---

# Skill: Drop-Off Format

## Purpose
A percentage without a count hides scale. A count without a percentage hides
severity. "We lost 12,000 users" sounds bad until you learn that's 3% of the
base. "34% drop-off" sounds bad until you learn that's 850 users out of 2,500.
This skill enforces one rule: **every drop-off shows three numbers.**

## When to Use
Before presenting ANY step-to-step drop-off — in a funnel table, in narrative
text, in a chart annotation, in a Slack message, or on a slide. This runs on
every output that contains funnel or conversion-step data.

## The Rule

> **Every drop-off must show: entering count, exiting count, and drop-off
> percentage.**

All three, every time. The format:

```
checkout_started (43,490) -> payment_attempted (35,543): 18.3% drop-off
```

In a table, this becomes three columns:

| Step | Users | Drop-off |
|------|-------|----------|
| checkout_started | 43,490 | -- |
| payment_attempted | 35,543 | 18.3% (7,947 lost) |

Either format is acceptable. What is not acceptable is showing only one or two
of the three numbers.

## Instructions

### Step 1: Find every drop-off in your draft output
Scan the response you are about to send. Every place where two adjacent funnel
steps are compared — in a table row, a sentence, a chart label — is in scope.

### Step 2: Check for all three numbers
For each drop-off, confirm you have:
1. **Entering count** — unique users at the upstream step
2. **Exiting count** — unique users at the downstream step
3. **Drop-off percentage** — `(entering - exiting) / entering x 100`

If any of the three is missing, add it before sending.

### Step 3: Verify the arithmetic
The percentage must equal `(entering - exiting) / entering x 100`, rounded to
one decimal place. Do the division — do not estimate. A wrong percentage is
worse than a missing one.

### Step 4: Apply to the "biggest leak" callout too
When the readout names the biggest drop-off, it must follow the same rule.
"The biggest leak is checkout_started -> payment_attempted" is incomplete.
"The biggest leak is checkout_started -> payment_attempted: 43,490 -> 35,543,
an 18.3% drop-off" is complete.

## Examples

### Bad -> Good

| Bad | Good |
|-----|------|
| "34% drop-off at checkout" | "checkout_started (43,490) -> payment_attempted (35,543): 18.3% drop-off" |
| "We lost 7,947 users at payment" | "payment_attempted lost 7,947 of 43,490 users (18.3%) from checkout_started" |
| "The biggest leak is 47%" | "The biggest leak is product_view -> add_to_cart: 49,899 -> 48,083, a 3.6% drop-off" |

## Anti-Patterns

1. **Never show only a percentage.** The reader cannot tell if 34% means 340
   users or 340,000.
2. **Never show only a raw count.** The reader cannot tell if 7,947 lost is
   catastrophic or routine without knowing the base.
3. **Never round the percentage to a whole number.** Use one decimal place.
   The difference between 18% and 18.3% matters when comparing steps.
4. **Never skip the rule for the "biggest leak" callout.** That line is the
   most-read sentence in the readout — it needs all three numbers more than
   any other.
