---
name: color-commentary
description: >-
  Every chart ships with 1-2 sentences of commentary, baked into the chart subtitle AND a sidecar
  .md, telling the reader what to NOTICE, not what the chart depicts. Trigger every time you save,
  render, embed, or caption any visual, and when presenting or re-sharing a chart that ALREADY
  EXISTS: regenerate it if its subtitle describes rather than reveals. Describing the chart does
  not satisfy this skill.
---

# Skill: Color Commentary

## Purpose
A chart shows everything and emphasizes nothing. The reader's eye goes to the
biggest bar — which is almost never the interesting part. Color commentary is the
analyst's voice pointing at the thing the chart contains but does not announce.

This skill enforces one rule: **every chart is followed by 1-2 sentences saying
what to notice.**

## When to Use
Immediately after rendering any chart, and before presenting it. This runs
alongside the other output skills:

- `visualization-patterns` builds the chart correctly (form, color, marks, themes).
- **`color-commentary` (this skill) says what the chart means.**
- `always-compare` verifies every number in that commentary carries an anchor.

## The Rule

> **Never ship a chart without 1-2 sentences below it telling the reader what to notice.
> Describe the insight, never the chart.**

The commentary sits **directly below the figure** — not in a footnote, not three
paragraphs later. It is the first thing read after the image.

## Where the commentary lives

Commentary written only into a chat reply **does not count**. Charts get shared —
dropped into Slack, pasted into decks, attached to tickets — and the moment the PNG
leaves the conversation, chat-only commentary is gone and the reader is back to
guessing. The insight has to travel with the file.

So every chart ships the commentary in **two places**:

| Where | What goes there | Why |
|---|---|---|
| **The chart's subtitle** (baked into the image) | The insight, compressed to one line | Survives being shared standalone. This is the slot most charts waste on a description. |
| **A sidecar `.md`** next to the image (`monthly_orders_2024.png` -> `monthly_orders_2024.md`) | The full 1-2 sentence commentary, the anchored numbers, and what it means for the decision | Room to say the whole thing; feeds reports and decks. |

The subtitle is the one that matters most, because it is the one that cannot get
separated from the chart. **The subtitle slot is for the insight, not the summary.**
If your subtitle would still be true with the data swapped out, you wasted it:

- Bad: `"Order volume grew 6.1x from January to December"` — describes the chart
- Good: `"November's +27% spike is Black Friday, not demand"` — tells you what to notice

## Reusing an existing chart

An existing chart is **not** grandfathered in. If you are about to present a chart
that already exists on disk — one you found, or one built in an earlier session —
run it through this skill before you show it:

1. Open the image and read its subtitle.
2. If the subtitle describes the chart rather than revealing something, **it fails
   this skill.** Regenerate the chart with a real insight in the subtitle.
3. If no sidecar `.md` exists, write one.

"The numbers are still correct" is not the bar. A numerically-correct chart with a
descriptive subtitle is exactly the chart this skill exists to prevent. Verifying
an old chart's data and shipping it unchanged means the skill never ran.

## The Test

Before you ship the commentary, ask:

> **Would a smart reader who already looked at the chart say "huh, I didn't catch that"
> — or "yes, I can read a chart"?**

If it's the second one, you wrote a caption, not commentary. Rewrite it.

## Instructions

### Step 1: Read your own chart like a stranger
Look at the rendered image. What does the eye land on first? That first impression
is the **surface reading** — and your commentary usually exists to complicate it,
qualify it, or overturn it.

### Step 2: Hunt for the thing the chart hides
Chart-reading is dominated by size. These are the places the point usually hides
instead — work down the list until something lands:

| Pattern | The question that finds it |
|---|---|
| **The denominator** | Is this raw count riding a growing base? Normalize it — does the trend survive? |
| **Growth vs. size** | The biggest bar and the fastest-growing bar are rarely the same one. Which is which? |
| **The distortion** | Is a period inflated by a promo, holiday, launch, outage, or backfill? (Check `.knowledge/datasets/{active}/quirks.md`.) |
| **The inflection** | Where does the trend *break*? The bend matters more than the slope. |
| **The dog that didn't bark** | What stayed flat that you expected to move? Absence is evidence. |
| **The scale illusion** | Is a dramatic-looking gap actually inside the noise band — or a small-looking one actually material? |
| **The composition** | Is the total moving because the mix changed rather than the level? |

### Step 3: Write it in the pivot shape
The strongest commentary has a **turn** in it — it grants the surface reading, then
redirects. Reach for these shapes:

- *"X looks like the story, but Y is the story."*
- *"The obvious read is A; zoom in and it's actually B."*
- *"Ignore the peak — the interesting part is C."*

### Step 4: Anchor it with a specific number
Vague commentary is worthless. "APAC is growing fast" is a vibe; "APAC grew 34% vs.
NA's 5%" is a finding. Cite the actual figures, and — per `always-compare` — make
sure each one carries its comparison.

### Step 5: Say what it means, if you know
The best final clause tells the reader what changes because of this. Not always
possible in two sentences; never pad to fake it.

### Step 6: If the chart is genuinely boring, say THAT honestly
Do not manufacture drama. A flat, unsurprising chart still has commentary — the
honest kind, which reports what the chart **rules out**:

> *"Nothing moves here: completion rate holds between 83.8% and 86.6% all year. That
> rules out order quality as an explanation for the Q4 revenue miss — look elsewhere."*

A null result, stated plainly, is a real contribution. A fabricated insight is not.

## Examples

### Bad -> Good

| Bad (describes the chart) | Good (tells you what to notice) |
|---|---|
| "This bar chart shows revenue by region." | "North America looks dominant, but zoom in: APAC grew 34% while NA grew just 5% — on this trajectory APAC passes NA within six quarters." |
| "Monthly orders increased through 2024." | "The 6.1x climb is mostly an illusion: the user base grew 14.6x over the same window, so orders per 1,000 users actually *fell* from 349 to 147." |
| "Conversion is highest on desktop." | "Desktop's 5.4% conversion is the headline, but mobile is 78% of traffic — so mobile's 2.1% is where nearly all the lost revenue actually lives." |
| "The funnel shows drop-off at each stage." | "Four of the five steps lose 10-15% as expected; checkout->payment loses 47%, and that single step accounts for more lost users than the other four combined." |
| "NPS by segment is shown below." | "Plus members score 12 points higher — but they're only 7% of respondents, so the site-wide 41 is really a story about the 93% who aren't members." |

### A full example, done right

> ![Monthly orders 2024](charts/monthly_orders_2024.png)
>
> *November spikes 27% over October — but that's Black Friday (25% off, Nov 25 - Dec 1),
> not demand. The signal to watch is December: it grew just 4.9% despite carrying a
> deeper, longer promotion, the weakest month of the year outside June.*

Two sentences. Names the distortion, then points past it to the thing that actually
matters. Every number anchored.

## Anti-Patterns

1. **Never describe the chart.** The reader has eyes. "Revenue by region," "trending upward," and "as you can see" are all noise. If the sentence would survive with the data swapped out, delete it.
2. **Never restate the title or axis labels.** They're already on the image.
3. **Never point at the biggest bar and stop.** That's the one thing the reader already saw without you.
4. **Never manufacture an insight.** If the chart is flat, report the null result and what it rules out — do not invent a trend that isn't there.
5. **Never write commentary without a number in it.** Specificity is the whole value; a number-free sentence is a vibe.
6. **Never exceed ~2 sentences.** This is a pointer, not the analysis. If it needs a paragraph, that paragraph belongs in the narrative *below* the commentary — the commentary still has to earn its two lines.
7. **Never bury it.** Directly under the figure or it doesn't count. Commentary in a footnote is commentary nobody reads.
8. **Never let its numbers escape `always-compare`.** Figures inside the commentary are metrics like any other and need their anchors.
9. **Never let the commentary live only in the chat reply.** If the insight dies the moment someone shares the PNG, you did not ship commentary — you made a remark. It goes in the subtitle and the sidecar `.md`.
10. **Never waste the subtitle on a description.** The subtitle is the most valuable text on the chart: it is the only commentary that cannot be separated from the image. A subtitle that restates the trend ("orders grew 6.1x") throws that away.
11. **Never grandfather an existing chart.** Presenting a chart you didn't just build — one found on disk or made in an earlier session — does not exempt it. Check its subtitle against this skill; regenerate it if it describes rather than reveals. Confirming the data is correct is not the same as confirming the chart is finished.
