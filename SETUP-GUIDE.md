# Setup Guide: Your First Analysis in Claude Cowork

This guide takes you from nothing to a finished analysis: a written brief and a chart, saved as files, built from your own data. Budget about 15 minutes.

## Step 1: Install Claude Desktop

1. Download the app from [claude.com/download](https://claude.com/download) and install it.
2. Sign in. Cowork requires a paid plan (Pro or above).
3. Open the app and look for **Cowork** in the sidebar.

## Step 2: Install the AI Analyst Plus plugin

1. In Cowork, go to **Customize > Plugins**.
2. Open **Plugins** from the left sidebar (the plug icon), click **Add**, then **Add marketplace**. Paste this repository URL and click **Sync**:

```
https://github.com/ai-analyst-lab/ai-analyst-plugin
```

Turn on **Sync automatically** if you want updates when the plugin improves. You will see a standard warning that marketplace plugins are not controlled by Anthropic; the code is public at the same link.
3. Find **AI Analyst Plus** in the list and click **Install**.

Two settings make the plugin reliable:

- **Add the global instruction.** In **Settings > Cowork (the instructions box), then Save**, paste this line: `For data analysis tasks, use the ai-analyst-plus skills and start from its decision-framing step.

One more habit that matters: start data questions with the /analyst command. Cowork chooses skills
per task on its own, and it will often skip installed skills on a casual question. /analyst invokes
the full method by name, every time. The global instruction above helps; the command is certain.` This applies to every session and makes sure analysis questions route to this plugin's method.
- **Disable the overlap.** If you have Anthropic's Data Analyst plugin installed, disable it while using this one. The two compete for the same tasks, and this one runs a stricter method.

## Step 3: Make a data folder

1. Create a new folder somewhere easy to find, for example `Documents/first-analysis`.
2. Put a data export in it. Good sources: a sales report from your point of sale system, an export from your CRM, a spreadsheet you already track things in.
3. CSV is the best format. Excel files also work.

Keep it to one or two files for your first run.

## Step 4: Work in the folder

1. In Cowork, choose **Project or folder > Add a folder** and pick the folder you just made.
2. Claude can now read the files in that folder and save new files into it. This folder is also where the plugin keeps its memory: a `.knowledge/` folder with dataset notes and logged corrections. Say yes when Claude offers to create it.

## Step 5: Ask a decision-shaped question

Type `/analyst` to start explicitly, or paste this template and fill in the blanks:

```
Look at the [data] in this folder, using [files].
I [role], and I need to decide [decision].
[Analysis ask].
Save me [deliverable].
If anything in the data looks off, flag it instead of smoothing over it.
```

The `[decision]` blank is the one that matters most. "I need to decide whether to keep the Tuesday promotion" gets you a real analysis. "Show me some insights" gets you trivia. If you leave the decision out, the plugin asks for it before analyzing.

Claude will profile your data first, tell you what it found, run the comparison, and save the brief and chart into your folder.

## Step 6: Run the three sanity checks

Before you act on the answer, check it. The plugin makes Claude show its checks, and you should push on them:

1. **Trace the headline number.** Ask: "Where exactly does that number come from? Which file, which column, which rows?" A real finding survives this question.
2. **Sum the parts.** If Claude broke a total into segments, ask: "Do the segments add back up to the total?" Mismatches reveal double counting or dropped rows.
3. **Compare against a number you already trust.** Tell Claude a number you know, like "we do about $40K a month", and ask it to compute the same thing from the data. If they disagree, sort that out before trusting anything else.


## Two things to expect on your first run

- The first analysis installs Python libraries (pandas, matplotlib, and friends) inside Cowork's
  workspace. That first run takes a few extra minutes. Later runs are fast.
- The analyst keeps its memory in a `.knowledge` folder inside your working folder. The first time
  you analyze in a new folder, it will offer to create that folder. Say yes: that is where your
  metric definitions and corrections live, and it is what makes the next run better than this one.

## Troubleshooting

- **Claude cannot read the file.** Keep files under 50 MB. If your export is bigger, filter it to a shorter date range before exporting.
- **The results look wrong.** Plain columnar CSVs work best: one header row, one record per row. Exports with merged cells, multiple sheets of summary tables, or title rows above the header confuse the profiling step. Re-export as a flat CSV.
- **Claude did not save files.** Make sure you picked **Project or folder > Add a folder** rather than attaching the file to a chat message.
- **The wrong skills fire.** Check that Anthropic's Data Analyst plugin is disabled and the global instruction from Step 2 is in place. `/analyst` always starts the AI Analyst Plus method explicitly.

## Go deeper

- The tutorial on customizing Cowork: [academy.claude.com/tutorials/customize-claude-cowork](https://academy.claude.com/tutorials/customize-claude-cowork)
- The free Academy course: Introduction to Claude Cowork, at [academy.claude.com](https://academy.claude.com)
- Live courses on AI analytics, where this plugin comes from: [maven.com/dataneighbor](https://maven.com/dataneighbor)
