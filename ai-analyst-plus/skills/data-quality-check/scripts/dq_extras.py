"""Data quality extras: source-agnostic DataFrame checks.

Standalone copy bundled with the data-quality-check skill (no repo imports;
needs only pandas and numpy). Combines the null-concentration and outlier
checks with the temporal-coverage and value-domain checks.

Usage (with this skill's scripts/ dir on sys.path):
    from dq_extras import (
        check_null_concentration, check_outliers, safe_check_outliers,
        check_temporal_coverage, check_value_domain,
    )
"""

import math

import numpy as np
import pandas as pd

def check_null_concentration(df, warn_threshold=0.05, fail_threshold=0.5):
    """Flag columns with high null concentrations.

    Severity follows the canonical null-severity table shared with
    ``structural_validator.validate_completeness`` and the
    data-quality-check skill text:

    - ``< 5%`` nulls: PASS
    - ``5-20%`` nulls: WARNING
    - ``> 20-50%`` nulls: SEVERE WARNING
    - ``> 50%`` nulls: BLOCKER

    ``status`` stays the coarse PASS/WARN/FAIL gate for existing callers
    (FAIL = BLOCKER band, WARN = either warning band); ``severity`` carries
    the canonical label.

    Args:
        df: pandas.DataFrame to check.
        warn_threshold: Fraction of nulls at or above which a column enters
            the WARNING band (default 0.05, the canonical table's edge).
        fail_threshold: Fraction of nulls above which a column is a
            BLOCKER/FAIL (default 0.5, the canonical table's edge).

    Returns:
        list of dicts with keys: column, null_count, null_pct, status,
        severity, detail
    """
    results = []
    n = len(df)
    if n == 0:
        return results

    for col in df.columns:
        null_count = int(df[col].isna().sum())
        null_pct = null_count / n

        if null_pct > fail_threshold:
            status, severity = "FAIL", "BLOCKER"
            detail = f"{null_pct:.1%} null — over half the values are missing"
        elif null_pct > 0.2:
            status, severity = "WARN", "SEVERE WARNING"
            detail = f"{null_pct:.1%} null: heavy null concentration"
        elif null_pct >= warn_threshold:
            status, severity = "WARN", "WARNING"
            detail = f"{null_pct:.1%} null: elevated null rate"
        else:
            status, severity = "PASS", "PASS"
            detail = f"{null_pct:.1%} null"

        results.append({
            "column": col,
            "null_count": null_count,
            "null_pct": round(null_pct, 4),
            "status": status,
            "severity": severity,
            "detail": detail,
        })

    return results


def check_outliers(series, method="iqr", iqr_multiplier=1.5, z_threshold=3.0):
    """Detect outliers in a numeric series using IQR or z-score method.

    Args:
        series: pandas.Series of numeric values.
        method: ``"iqr"`` (interquartile range) or ``"zscore"``.
        iqr_multiplier: Multiplier for IQR fences (default 1.5).
        z_threshold: Z-score threshold for outlier detection (default 3.0).

    Returns:
        dict with keys: method, n_outliers, n_total, outlier_pct, bounds,
        status, detail, outlier_indices
    """
    clean = series.dropna()
    n_total = len(clean)

    if n_total < 4:
        return {
            "method": method,
            "n_outliers": 0,
            "n_total": n_total,
            "outlier_pct": 0.0,
            "bounds": None,
            "status": "WARN",
            "detail": f"Too few non-null values ({n_total}) for outlier detection",
            "outlier_indices": [],
        }

    if method == "iqr":
        q1 = float(clean.quantile(0.25))
        q3 = float(clean.quantile(0.75))
        iqr = q3 - q1
        lower = q1 - iqr_multiplier * iqr
        upper = q3 + iqr_multiplier * iqr
        mask = (clean < lower) | (clean > upper)
        bounds = {"lower": round(lower, 4), "upper": round(upper, 4)}
    elif method == "zscore":
        mean = float(clean.mean())
        std = float(clean.std())
        if std == 0:
            return {
                "method": method,
                "n_outliers": 0,
                "n_total": n_total,
                "outlier_pct": 0.0,
                "bounds": None,
                "status": "PASS",
                "detail": "Zero variance — no outliers possible",
                "outlier_indices": [],
            }
        z_scores = (clean - mean) / std
        mask = z_scores.abs() > z_threshold
        bounds = {
            "lower": round(mean - z_threshold * std, 4),
            "upper": round(mean + z_threshold * std, 4),
        }
    else:
        raise ValueError(f"Unknown method: {method}. Use 'iqr' or 'zscore'.")

    outlier_indices = list(clean[mask].index)
    n_outliers = len(outlier_indices)
    outlier_pct = round(n_outliers / n_total, 4) if n_total > 0 else 0.0

    if n_outliers == 0:
        status, detail = "PASS", "No outliers detected"
    elif outlier_pct < 0.05:
        status = "PASS"
        detail = f"{n_outliers} outliers ({outlier_pct:.1%}) — within normal range"
    elif outlier_pct < 0.15:
        status = "WARN"
        detail = f"{n_outliers} outliers ({outlier_pct:.1%}) — elevated"
    else:
        status = "FAIL"
        detail = f"{n_outliers} outliers ({outlier_pct:.1%}) — unusually high"

    return {
        "method": method,
        "n_outliers": n_outliers,
        "n_total": n_total,
        "outlier_pct": outlier_pct,
        "bounds": bounds,
        "status": status,
        "detail": detail,
        "outlier_indices": outlier_indices[:20],  # cap for display
    }


def safe_check_outliers(series, method="iqr", **kwargs):
    """Student-safe wrapper around ``check_outliers()``. Never raises."""
    try:
        return check_outliers(series, method=method, **kwargs)
    except Exception as exc:
        return {
            "method": method,
            "n_outliers": 0,
            "n_total": len(series) if hasattr(series, "__len__") else 0,
            "outlier_pct": 0.0,
            "bounds": None,
            "status": "WARN",
            "detail": f"Could not check outliers: {exc}",
            "outlier_indices": [],
        }


def check_temporal_coverage(df, date_col, freq="D", max_gap_tolerance=1):
    """Check for gaps in a time series.

    Computes the expected date range at the given frequency and identifies
    missing periods. Useful for detecting data ingestion failures or
    incomplete time ranges.

    Args:
        df: DataFrame containing the date column.
        date_col: Name of the date/datetime column.
        freq: Expected frequency — ``"D"`` (daily), ``"W"`` (weekly),
            ``"M"`` (monthly), ``"H"`` (hourly).
        max_gap_tolerance: Number of consecutive missing periods before
            a gap is flagged. Default 1 (flag any single missing period).

    Date columns stored as YYYYMMDD integers are parsed with an explicit
    ``%Y%m%d`` format (noted in the message); any other numeric dtype
    returns FAIL instead of being silently coerced to
    nanoseconds-since-epoch.

    Returns:
        dict with keys: status, message, details
    """
    col = df[date_col]
    dtype_note = None

    if pd.api.types.is_numeric_dtype(col):
        vals = col.dropna()
        looks_yyyymmdd = (
            len(vals) > 0
            and bool(((vals % 1) == 0).all())
            and bool(vals.between(10000101, 99991231).all())
        )
        if not looks_yyyymmdd:
            return {
                "status": "FAIL",
                "message": (
                    f"Column '{date_col}' has numeric dtype '{col.dtype}' "
                    f"that cannot be interpreted as dates (values do not "
                    f"look like YYYYMMDD integers). Convert the column to "
                    f"datetime explicitly before checking coverage."
                ),
                "details": {"date_col": date_col, "dtype": str(col.dtype)},
            }
        dates = pd.to_datetime(
            vals.astype("int64").astype(str), format="%Y%m%d", errors="coerce"
        ).dropna()
        dtype_note = (
            f"Note: '{date_col}' stores dates as {col.dtype} YYYYMMDD "
            f"integers; parsed with format='%Y%m%d'."
        )
    else:
        dates = pd.to_datetime(col, errors="coerce").dropna()

    if len(dates) < 2:
        return {
            "status": "WARN",
            "message": f"Too few dates in '{date_col}' to check coverage.",
            "details": {"date_col": date_col, "valid_dates": len(dates)},
        }

    date_min = dates.min()
    date_max = dates.max()

    # Generate expected date range
    expected = pd.date_range(start=date_min, end=date_max, freq=freq)
    actual_periods = set(dates.dt.to_period(freq))
    expected_periods = set(expected.to_period(freq))
    missing = sorted(expected_periods - actual_periods)

    # Group consecutive missing periods into gaps
    gaps = []
    if missing:
        gap_start = missing[0]
        gap_end = missing[0]
        for period in missing[1:]:
            if period.ordinal - gap_end.ordinal <= 1:
                gap_end = period
            else:
                gap_len = gap_end.ordinal - gap_start.ordinal + 1
                if gap_len > max_gap_tolerance:
                    gaps.append({
                        "start": str(gap_start),
                        "end": str(gap_end),
                        "missing_periods": gap_len,
                    })
                gap_start = period
                gap_end = period
        # Final gap
        gap_len = gap_end.ordinal - gap_start.ordinal + 1
        if gap_len > max_gap_tolerance:
            gaps.append({
                "start": str(gap_start),
                "end": str(gap_end),
                "missing_periods": gap_len,
            })

    n_missing = len(missing)
    n_expected = len(expected_periods)
    coverage_pct = round(100 * (1 - n_missing / n_expected), 2) if n_expected > 0 else 100.0

    details = {
        "date_col": date_col,
        "freq": freq,
        "range": f"{date_min.date()} to {date_max.date()}",
        "expected_periods": n_expected,
        "actual_periods": n_expected - n_missing,
        "missing_periods": n_missing,
        "coverage_pct": coverage_pct,
        "gaps": gaps[:10],  # cap display
    }
    if dtype_note:
        details["dtype_note"] = dtype_note

    def _msg(text):
        return f"{text} {dtype_note}" if dtype_note else text

    if n_missing == 0:
        return {
            "status": "PASS",
            "message": _msg(
                f"Full temporal coverage for '{date_col}' ({coverage_pct}%)."
            ),
            "details": details,
        }
    elif coverage_pct >= 95:
        return {
            "status": "WARN",
            "message": _msg(
                f"Minor gaps in '{date_col}': {n_missing} missing {freq} "
                f"periods ({coverage_pct}% coverage)."
            ),
            "details": details,
        }
    else:
        return {
            "status": "FAIL",
            "message": _msg(
                f"Significant gaps in '{date_col}': {n_missing} missing {freq} "
                f"periods ({coverage_pct}% coverage). {len(gaps)} gap(s) found."
            ),
            "details": details,
        }


def check_value_domain(series, expected_values, allow_null=True):
    """Check that a categorical column contains only expected values.

    Args:
        series: pandas.Series of categorical values.
        expected_values: Set or list of allowed values.
        allow_null: If True, NaN/None values are ignored. If False,
            nulls count as unexpected values.

    Returns:
        dict with keys: status, message, details
    """
    expected = set(expected_values)
    actual = set(series.dropna().unique()) if allow_null else set(series.unique())
    unexpected = actual - expected
    missing_expected = expected - actual

    details = {
        "expected_values": sorted(str(v) for v in expected),
        "actual_values": sorted(str(v) for v in actual),
        "unexpected_values": sorted(str(v) for v in unexpected),
        "missing_expected": sorted(str(v) for v in missing_expected),
        "n_unexpected_rows": 0,
    }

    if unexpected:
        unexpected_mask = series.isin(unexpected)
        details["n_unexpected_rows"] = int(unexpected_mask.sum())

    if not unexpected and not missing_expected:
        return {
            "status": "PASS",
            "message": f"All values match expected domain ({len(expected)} values).",
            "details": details,
        }
    elif unexpected:
        return {
            "status": "FAIL",
            "message": (
                f"Found {len(unexpected)} unexpected value(s): "
                f"{sorted(str(v) for v in list(unexpected)[:5])}. "
                f"{details['n_unexpected_rows']:,} rows affected."
            ),
            "details": details,
        }
    else:
        # Only missing_expected (no unexpected) — domain is a subset
        return {
            "status": "WARN",
            "message": (
                f"Data covers {len(actual)}/{len(expected)} expected values. "
                f"Missing: {sorted(str(v) for v in list(missing_expected)[:5])}."
            ),
            "details": details,
        }
