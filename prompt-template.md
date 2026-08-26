# The Decision-Shaped Prompt

Copy this, fill in the blanks, and paste it into Cowork after choosing your data folder. Start with /analyst so the full method runs by name.

```
/analyst Look at the [data] in this folder, using [files].
I [role], and I need to decide [decision].
[Analysis ask].
Save me [deliverable].
If anything in the data looks off, flag it instead of smoothing over it.
```

## What each blank does

| Blank | What to put there | Why it matters |
|---|---|---|
| `[data]` | What the data is, in plain words: "coffee shop sales data", "our support ticket export" | Gives Claude the business context the columns alone cannot |
| `[files]` | The exact file names to use | Keeps Claude off stray files in the folder |
| `[role]` | Who you are: "run the shop", "am the head of support" | Sets the level of detail and language in the deliverable |
| `[decision]` | What you will do differently based on the answer | The most important blank. It sets the scope and the comparison |
| `[Analysis ask]` | The specific comparison or breakdown you want | Turns "insights please" into an answerable question |
| `[deliverable]` | What you want handed back: "a one page brief and one chart" | You get files you can share, not just chat |

The last line is not decoration. It gives Claude standing permission to bring you bad news about the data, which is exactly when you most need an analyst.

## A filled-in example

```
/analyst Look at the coffee shop sales data in this folder, using sales_2025.csv.
I run the shop, and I need to decide whether to keep the Tuesday pastry promotion.
Compare Tuesday sales before and after the promotion started in June,
and check whether the lift holds outside of pastries.
Save me a one page brief and one chart.
If anything in the data looks off, flag it instead of smoothing over it.
```
