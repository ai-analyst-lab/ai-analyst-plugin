# Skill: Forecast

## Purpose
Generate time-series forecasts for key metrics using the forecast_helpers
library. Supports naive baselines, seasonality detection, and exponential
smoothing — enough to answer "what should we expect next?" without complex
modeling.

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

### Step 1: Prepare the Data
1. Identify the metric and its source table from the metric dictionary
   (`.knowledge/datasets/{active}/metrics/`) or from user specification.
2. Query the data aggregated to the appropriate granularity (daily/weekly/monthly).
3. Create a pandas Series with DatetimeIndex.
4. Clean: forward-fill NaN, drop leading nulls.
5. Require at least 14 data points. If fewer: "Not enough history for forecasting."

### Step 2: Detect Seasonality
Run `detect_seasonality()` from `helpers/forecast_helpers.py`:
- If seasonality detected, report: "Found {strength} {period}-day seasonality."
- Store the dominant period for use in Step 3.

### Step 3: Generate Forecasts
Run multiple methods and compare:

1. **Naive (last value):** `naive_forecast(series, periods, method='last')`
2. **Naive (seasonal):** If seasonality detected: `naive_forecast(series, periods, method='seasonal_naive')`
3. **Exponential smoothing (auto):** `exponential_smoothing(series)`
4. **Holt-Winters:** If seasonality detected and enough data: `exponential_smoothing(series, seasonal_period=dominant_period)`

Compare MSE across methods. Select the best-fit method.

### Step 4: Generate Chart
Using `chart_helpers`:
1. Call `swd_style()`
2. Plot historical data as a solid line
3. Plot forecast as a dashed line with lighter alpha
4. Add confidence band (±1 std of residuals) as shaded area
5. Mark the historical/forecast boundary with a vertical dashed line
6. Use `action_title()` with a forward-looking title
7. Save to `working/forecast_{metric}_{DATE}.png` using `save_chart()`

### Step 5: Present Results
Report:
- Best method and why (lowest MSE)
- Forecast values for key periods (next 7/14/30 days)
- Seasonality summary
- Confidence level (based on residual magnitude)
- Caveats: "Forecasts assume past patterns continue. External factors not modeled."

## Rules
1. Always run at least 2 methods for comparison
2. Never present a forecast without stating assumptions
3. Always include a naive baseline so the user can see if the model adds value
4. Flag if residuals show systematic patterns (model may be misspecified)
5. If the data has a structural break, warn that forecasts may be unreliable

## Edge Cases
- **Constant series:** Report "No variation — forecast is the constant value"
- **Strong trend + no seasonality:** Use Holt's (double) exponential smoothing
- **Very short history (<30 points):** Only use naive methods, warn about accuracy
- **Data gaps:** Interpolate or warn, depending on gap size
