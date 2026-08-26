# AI Analyst Plus for Claude Cowork

Point Claude at a folder with data, ask a decision-shaped question, and it works like a careful analyst: frames the decision, profiles the data before trusting it, pairs every number with a comparison, traces findings to source, validates before presenting, and saves real deliverables (briefs, charts) into your folder. A `.knowledge/` folder inside your working folder acts as memory: dataset notes, quirks, and logged corrections that persist across sessions, so a mistake corrected once is never repeated.

Under the hood it is roughly 45 skills covering decision framing, data profiling, validated analysis, experimentation, causal inference, visualization, and storytelling, ported from the Claude Code analyst system used in the AI Analytics courses.

Two entry points:

- **Automatic.** Ask any data question. The `analyst-core` skill fires on analytical intent and steers the session through the method.
- **Explicit.** Type `/analyst` (optionally with your question) to start an analysis the AI Analyst way from the first message.

## Install in Claude Cowork

1. Open Cowork in the Claude desktop app.
2. Go to **Customize > Plugins > Add marketplace**.
3. Paste this repository: `ai-analyst-lab/ai-analyst-plugin`
4. Find **AI Analyst Plus** and click **Install**.

New to Cowork? The walkthrough, from installing Claude Desktop to your first analysis, is in [SETUP-GUIDE.md](./SETUP-GUIDE.md).

## Install in Claude Code

```bash
claude plugin marketplace add ai-analyst-lab/ai-analyst-plugin
claude plugin install ai-analyst-plus@ai-analyst-plugin
```

## How to use it

1. Make a folder containing a data export (CSV works best).
2. In Cowork, choose **Work in a folder** and pick that folder.
3. Ask a decision-shaped question, or run `/analyst`. The fill-in-the-blanks template is in [prompt-template.md](./prompt-template.md).

Claude profiles the data, runs the analysis, and saves a brief and charts into the folder, with a Checks section stating what was verified and what was not.

## Avoid a selection conflict

If you also have Anthropic's Data Analyst plugin installed, both plugins trigger on the same tasks, so disable whichever one you are not using at the moment. If you want this plugin's method to be the default, add one line to **Settings > Cowork > Global instructions**:

> For data analysis tasks, use the ai-analyst-plus skills and start from its decision-framing step.

## What is NOT here

This plugin is the analysis method and the skills that carry it. The fuller system the maintainers run also includes automated multi-step orchestration (pipelines that run, resume, and archive whole analyses), a maintained eval suite with curated gold sets, and heavier statistical tooling beyond the core pandas and scipy stack; none of that is included here. Skills that existed only to operate that machinery, or that depend on local setup Cowork does not have, were left out of the port; in particular, warehouse access now goes through Cowork connectors via the connect-data skill instead of hand-configured connections. Two skills, show-off and north-star, were removed in the production pass; north-star because its reference corpus is not ours to redistribute. The full system is taught in the Agentic Analytics course at [maven.com/dataneighbor](https://maven.com/dataneighbor).

## Make it yours

The skills get better with your context: your metric definitions, your data quirks, the numbers your team already trusts. Edit the SKILL.md files in `ai-analyst-plus/skills/` directly, or let the `.knowledge/` folder accumulate that context as you work.

## License

MIT. See [LICENSE](./LICENSE).

Built by [Shane Butler](https://maven.com/dataneighbor) at AI Analyst Lab, ported from the analyst system used in the AI Analytics courses.
