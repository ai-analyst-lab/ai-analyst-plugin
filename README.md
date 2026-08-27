<div align="center"><pre>
 █████╗ ██╗     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗████████╗
██╔══██╗██║    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝██╔════╝╚══██╔══╝
███████║██║    ███████║██╔██╗ ██║███████║██║   ╚████╔╝ ███████╗   ██║   
██╔══██║██║    ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝  ╚════██║   ██║   
██║  ██║██║    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████║   ██║   
╚═╝  ╚═╝╚═╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝   ╚═╝   
                   ██████╗ ██╗     ██╗   ██╗███████╗                    
                   ██╔══██╗██║     ██║   ██║██╔════╝                    
                   ██████╔╝██║     ██║   ██║███████╗                    
                   ██╔═══╝ ██║     ██║   ██║╚════██║                    
                   ██║     ███████╗╚██████╔╝███████║                    
                   ╚═╝     ╚══════╝ ╚═════╝ ╚══════╝                    
</pre>

<strong>An AI data analyst you run inside Claude Cowork or Claude Code.</strong>

<img src="https://img.shields.io/badge/skills-47-D97706"> <img src="https://img.shields.io/badge/agents-13-D97706"> <img src="https://img.shields.io/badge/runs%20in-Claude%20Cowork%20%C2%B7%20Claude%20Code-8A2BE2"> <img src="https://img.shields.io/badge/license-MIT-3da639">

decision framing · data profiling · validated analysis · saved briefs and charts · memory that persists

<a href="#what-it-does">What it does</a> ·
<a href="#install-in-claude-cowork">Install</a> ·
<a href="#how-to-use-it">How to use it</a> ·
<a href="#what-is-not-here">What's not here</a> ·
<a href="https://youtu.be/YNlAGcpgW-k">Watch the walkthrough</a> ·
<a href="https://join.slack.com/t/aianalystlab/shared_invite/zt-3yhcg5cit-WnENO3sWfnvro6kvDqQNgA">Slack</a> ·
<a href="https://aianalystlab.ai">Website</a>
</div>

---

## What it does

Point Claude at a folder with data, ask a decision-shaped question, and it works like a careful analyst: frames the decision, profiles the data before trusting it, pairs every number with a comparison, traces findings to source, validates before presenting, and saves real deliverables (briefs, charts) into your folder. A `.knowledge/` folder inside your working folder acts as memory: dataset notes, quirks, and logged corrections that persist across sessions, so a mistake corrected once is never repeated.

Under the hood it is 47 skills and 13 agents covering decision framing, data profiling, validated analysis, experimentation, causal inference, visualization, and storytelling, ported from the Claude Code analyst system used in the AI Analytics courses.

Two entry points:

- **Explicit (the reliable path).** Type `/analyst` with your question. The full method runs by name from the first message: framing, checks, brief.
- **Automatic.** Cowork picks skills per task on its own and sometimes skips them on casual questions. The global-instruction line under [How to use it](#how-to-use-it) makes automatic selection lean this way.

## Install in Claude Cowork

1. Open the Claude desktop app and click **Cowork** in the prompt bar.
2. Open **Plugins** from the left sidebar (the plug icon), then **Add > Add marketplace**.
3. Paste this URL and click **Sync**:

   ```
   https://github.com/ai-analyst-lab/ai-analyst-plugin
   ```

4. **AI Analyst Plus** now appears under **Your plugins**.

New to Cowork? The walkthrough, from installing Claude Desktop to your first analysis, is in [SETUP-GUIDE.md](./SETUP-GUIDE.md), and the recorded session that builds an analyst end to end is on [YouTube](https://youtu.be/YNlAGcpgW-k).

## Install in Claude Code

```bash
claude plugin marketplace add ai-analyst-lab/ai-analyst-plugin
claude plugin install ai-analyst-plus@ai-analyst-plugin
```

## How to use it

1. Make a folder containing a data export (CSV works best).
2. In Cowork, click **Project or folder** under the prompt bar, choose **Add a folder**, and pick that folder.
3. Start your question with `/analyst`. The fill-in-the-blanks template is in [prompt-template.md](./prompt-template.md).

Claude profiles the data, runs the analysis, and saves a brief and charts into the folder, with a Checks section stating what was verified and what was not.

To make the method the default for every analysis task, add one line to **Settings > Cowork** instructions:

> For data analysis tasks, use the ai-analyst-plus skills and start from its decision-framing step.

One more note: if you also have Anthropic's Data Analyst plugin installed, both trigger on the same tasks. Disable whichever one you are not using at the moment.

## What is NOT here

This plugin is the analysis method and the skills that carry it. The fuller system the maintainers run also includes automated multi-step orchestration (pipelines that run, resume, and archive whole analyses), a maintained eval suite with curated gold sets, and heavier statistical tooling beyond the core pandas and scipy stack; none of that is included here. Skills that existed only to operate that machinery, or that depend on local setup Cowork does not have, were left out of the port; in particular, warehouse access now goes through Cowork connectors via the connect-data skill instead of hand-configured connections. Two skills, show-off and north-star, were removed in the production pass; north-star because its reference corpus is not ours to redistribute. The full system is taught in the Agentic Analytics course at [maven.com/dataneighbor](https://maven.com/dataneighbor).

## Make it yours

The skills get better with your context: your metric definitions, your data quirks, the numbers your team already trusts. Edit the SKILL.md files in `ai-analyst-plus/skills/` directly, or let the `.knowledge/` folder accumulate that context as you work.

## License

MIT. See [LICENSE](./LICENSE).

Built by [Shane Butler](https://maven.com/dataneighbor) at AI Analyst Lab, ported from the analyst system used in the AI Analytics courses.
