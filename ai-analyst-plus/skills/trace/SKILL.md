---
name: trace
description: >-
  Show the provenance of every reported number: which query or computation produced it, from which
  file or table. Use after an analysis when someone asks "where did that number come from?", "show
  your work", "prove it", or "/trace". Also use proactively before a deliverable ships, as part of
  the check-before-sharing pass.
---

# /trace: tie every number to its source

## Purpose
Answer "where did that number come from?" with evidence, not memory. Every number in a brief or
readout gets linked to the exact computation and source data that produced it.

## When to Use
- The user asks where a number came from, or to show the work.
- Before any deliverable leaves the session (analyst-core rule: trace numbers to source).
- Reviewing an analysis produced earlier in the session or found in `.knowledge/analyses/`.

## Instructions

1. **Collect the findings.** List every specific number in the deliverable being traced: headline
   figures, table cells that carry the argument, chart values called out in text.

2. **Collect the computations.** Gather the queries and code run this session (re-read your own
   steps; if the analysis logged queries to `.knowledge/query-log.md`, read that too).

3. **Build the trace table** and include it in the output (or save as `trace.md` next to the
   deliverable if the user wants a file):

   | # | Number | Where it appears | Produced by | Source data | Confidence |
   |---|---|---|---|---|---|
   | 1 | $1.2M | brief, headline | SUM(amount) over Q2 orders query | orders.csv | cited |

   Confidence labels:
   - **cited**: the computation for this number was run this session and is shown.
   - **value-match**: a run computation produced this value, but the deliverable did not name it.
   - **inferred**: no run computation produced it; state where it came from (an input doc, an
     assumption) or mark it unverified.

4. **Surface the gaps loudly.** Unverified numbers and orphan queries (run but unused) are the
   most important rows. Never hide them. If a headline number is inferred or unverified, say so
   at the top of the trace, not in a footnote.

5. **Offer the fix.** For any unverified number, offer to recompute it live from the source data
   so it can be promoted to cited.

## Notes
- This is a reading-and-reporting skill: no scripts, no extra infrastructure. The evidence is the
  session's own work plus the files in the working folder.
- Pairs with the reconcile check (parts sum to totals) and the reliability skill (run it again).
