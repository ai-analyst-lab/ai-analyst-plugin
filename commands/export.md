# Skill: Export

## Purpose
Export analysis results in different formats for different audiences. Converts
pipeline outputs into ready-to-share deliverables.

## When to Use
- User says `/export` or "export this as..." or "send this to..."
- After completing an analysis or pipeline run
- When the user needs results in a specific format

## Invocation
`/export slides` — generate/refresh Marp slide deck from latest analysis
`/export email` — write an executive summary email (markdown)
`/export slack` — write a concise Slack update (markdown)
`/export brief` — write a 1-page decision brief (markdown)
`/export data` — export analysis data tables as CSV
`/export all` — generate all text formats + data

## Instructions

### Step 1: Find Source Material
Check for completed analysis outputs in order of preference:
1. `outputs/slides_*.md` — latest deck
2. `outputs/analysis_*.md` — latest narrative
3. `working/pipeline_summary.md` — pipeline summary
4. `working/storyboard_*.md` — storyboard

If no outputs exist:
- Check `working/` for partial results
- If nothing found: "No analysis results to export. Run an analysis first or use `/run-pipeline`."

### Step 2: Generate Requested Format

**Format: slides**
- If deck already exists, ask: "Deck found at {path}. Regenerate or export as-is?"
- If no deck, invoke Deck Creator agent with latest narrative + charts
- Output: `outputs/slides_{DATE}.md`

**Format: email**
- Structure: Subject line + 3-paragraph body (context, key finding, recommendation)
- Tone: Executive-friendly, no jargon, action-oriented
- Include: 1-2 key numbers, the "so what", and a clear ask
- Output: `outputs/email_summary_{DATE}.md`

**Format: slack**
- Structure: Bold headline + 3-5 bullet points + thread-friendly
- Keep under 300 words
- Use emoji sparingly (checkmarks, arrows only)
- Include: key metric, direction, and recommended action
- Output: `outputs/slack_update_{DATE}.md`

**Format: brief**
- Structure: Title + Executive Summary (3 sentences) + Key Findings (numbered) +
  Recommendation + Next Steps + Appendix (data sources, methodology)
- 1 page target (~500 words)
- Output: `outputs/decision_brief_{DATE}.md`

**Format: data**
- Export all DataFrames from `working/` as CSVs to `outputs/data/`
- Include a README listing each file and its contents
- Output: `outputs/data/` directory

**Format: all**
- Run email + slack + brief + data sequentially
- Skip slides if already exists

### Step 3: Post-Export
- List all exported files with paths
- Suggest: "Copy the email to your clipboard?" or "Want to adjust the tone?"

## Rules
1. Never fabricate findings — only use data from actual analysis outputs
2. Always cite the source analysis date and dataset
3. Adapt detail level to format (email = high-level, brief = medium, data = raw)
4. Apply Stakeholder Communication skill for all text outputs
5. If the analysis had confidence scores, include them in brief format

## Edge Cases
- **Partial analysis:** Export what's available, note gaps: "Note: validation step was not completed."
- **Multiple analyses in outputs/:** Use the most recent by date, or ask user which one
- **Charts missing:** Text formats still work, note: "Charts not available for this export."
- **User requests unknown format:** List available formats and ask to choose
