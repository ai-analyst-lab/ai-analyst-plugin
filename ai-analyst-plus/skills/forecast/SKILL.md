---
name: forecast
description: >-
  Generate time-series forecasts and projections for metrics. Trigger on "/forecast", "what will X
  look like next month?", "forecast DAU for Q2", "project revenue", "estimate future growth",
  "predict next quarter", "where are we headed?", "extrapolate this trend", "what will happen if
  this continues?". Handles seasonality detection, model selection, confidence intervals, and
  validation against naive baselines.
---

# Skill: Forecast

## Purpose
Generate time-series forecasts for key metrics using the forecasting library
bundled with this skill (`scripts/forecast_helpers.py`). Supports naive


**If the skill install path cannot be resolved** (some sandboxed environments): read the script file(s) from this skill, write a copy into a `scripts/` folder inside the working folder, and run from there. The scripts are self-contained.
baselines, seasonality detection, and exponential smoothing — enough to answer
"what should we expect next?" without complex modeling.

## When to Use
- User asks "what will revenue look like next month?" or "forecast DAU"
- After trend analysis reveals a pattern worth projecting
- When sizing an opportunity that depends on future values
- Invoked as `/forecast`

## Invocation
`/forecast {metric}` — forecast the named metric
`/forecast {metric} periods=30` — specify forecast horizon
`/forecast {metric} method=holt_winters` — specify method

## Instructions

### Step 0: Understand the Business Context
Before diving into the forecast, ask clarifying questions if the user hasn't specified:
- **What decision depends on this forecast?** (e.g., capacity planning, budgeting, staffing, resource allocation)
- **Who will use it?** (exec summary vs technical deep-dive)
- **What's the forecast horizon?** (7 days, 30 days, 90 days, a quarter?)
- **Are there known upcoming changes?** (product launches, campaigns, seasonal events that would invalidate "business as usual" assumptions)

This context shapes how you present results. Capacity planning needs volume impacts and staffing recommendations. Budget planning needs totals and scenario ranges. Executive audiences need decision-focused summaries.

### Step 1: Prepare the Data
1. Identify the metric and its source table from the metric dictionary
   (`.knowledge/datasets/{active}/metrics/`) or from user specification.
2. Query the data aggregated to the appropriate granularity (daily/weekly/monthly).
3. Create a pandas Series with DatetimeIndex.
4. Clean: forward-fill NaN, drop leading nulls.
5. **Validate data sufficiency:** Require at least 14 data points for short-term forecasts, 30+ for seasonal forecasts, 60+ for quarterly projections. If insufficient, report: "Not enough history for forecasting — need at least {required} points, have {actual}." Explain what additional data would enable (e.g., "With 30+ days we could detect weekly seasonality").

### Step 2: Detect Seasonality
Run `detect_seasonality()` from the bundled `scripts/forecast_helpers.py` (add
On trending series, detrend first (subtract a fitted linear trend) before the ACF scan; a strong trend can swamp the seasonal signal at lag 12.
this skill's `scripts/` directory to `sys.path`, then
`from forecast_helpers import detect_seasonality, naive_forecast, exponential_smoothing`):
- If seasonality detected, report: "Found {strength} {period}-day seasonality."
- Store the dominant period for use in Step 3.

### Step 3: Generate Forecasts
Run multiple methods and compare:

1. **Naive (last value):** `naive_forecast(series, periods, method='last')`
2. **Naive (seasonal):** If seasonality detected: `naive_forecast(series, periods, method='seasonal_naive', seasonal_period=dominant_period)`. Always pass the detected period; if no cycle is given or inferable the function raises a ValueError rather than guessing a cycle.
3. **Exponential smoothing (auto):** `exponential_smoothing(series, forecast_periods=periods)`; the `forecast` key in the result holds the future values (holt-style continuation from the final fitted state).
4. **Holt-Winters:** If seasonality detected and enough data: `exponential_smoothing(series, seasonal_period=dominant_period, forecast_periods=periods)`

Compare MSE across methods and select the best-fit method. Every candidate above produces future values (`result["forecast"]`), so the selected method is always one that can actually forecast, not just fit.

### Step 4: Generate Chart
Build the chart with matplotlib, following the visualization-patterns skill's SWD style:
1. Apply the SWD base style first (warm off-white `#F7F6F2` figure and axes background, no top/right spines, no grid, sans-serif, dpi 150)
2. Plot historical data as a solid line (Action Amber `#D97706`, linewidth 2)
3. Plot forecast as a dashed line with lighter alpha
4. Add confidence band (±1 std of residuals) as shaded area
5. Mark the historical/forecast boundary with a vertical dashed line
6. Give it a bold left-aligned action title stating the forward-looking takeaway (optional gray subtitle for context)
7. Save to `working/forecast_{metric}_{DATE}.png` with `fig.savefig(path, dpi=150, bbox_inches="tight")` and close the figure

### Step 5: Present Results
Structure the output based on business context from Step 0:

**Always include:**
- Data validation summary: "{N} days of historical data analyzed, sufficient for {horizon}-day forecast"
- Best method and why (lowest MSE on validation holdout)
- Seasonality findings (if detected)
- Forecast values for key milestones (next 7/14/30/60/90 days as relevant)
- Confidence intervals (±1σ and ±2σ)
- Standard caveats: "Forecasts assume past patterns continue. External factors not modeled."

**Business context translation:**
- **Capacity planning:** Translate forecast to volume impacts (e.g., "+4% conversion → +4% order volume → scale fulfillment by 4%"). Provide staffing/resource recommendations with risk buffers.
- **Budget planning:** Provide period totals (monthly, quarterly) with upside/downside scenarios. Include sensitivity to key assumptions.
- **Monitoring/alerting:** Suggest thresholds for when actuals diverge from forecast (e.g., "If Week 1 revenue < $X, revisit assumptions").
- **Exec summary:** Lead with the decision implication, then support with numbers. Example: "No team scaling needed — conversion increase (+4% over 2 weeks) is within current capacity."

The forecast numbers are necessary but not sufficient. Your job is to answer "so what?" for the user's planning context.

## Rules
1. **Always run at least 2 methods for comparison.** The user needs to know the forecast isn't arbitrary — showing that one method outperforms others builds confidence.
2. **Never present a forecast without stating assumptions.** Every forecast has an expiration date and boundary conditions. Make them explicit.
3. **Always include a naive baseline.** Users need to see if the model adds value beyond "just use the last value." If naive performs nearly as well, say so — simpler is better.
4. **Flag if residuals show systematic patterns.** Autocorrelated residuals mean the model is missing something (trend, seasonality, structural break). Don't paper over this — it affects forecast reliability.
5. **If the data has a structural break, warn that forecasts may be unreliable.** A sudden spike or drop in the last N days means the historical pattern may not continue. Surface this uncertainty.
6. **Translate to business impact automatically.** Don't just report "4.09% conversion on Day 14" — connect it to the planning question: "4.09% conversion (+4% vs today) means approximately +4% order volume, which is within your current fulfillment capacity." The forecast is a means to a decision, not the end goal.

## Edge Cases
- **Constant series:** Report "No variation — forecast is the constant value"
- **Strong trend + no seasonality:** Use Holt's (double) exponential smoothing
- **Very short history (<30 points):** Only use naive methods, warn about accuracy
- **Data gaps:** Interpolate or warn, depending on gap size
