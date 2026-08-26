# Statistical Distributions Reference (compact)

Companion reference for the distribution-profiler skill. Read the Identification
Flowchart first, then only the card for the distribution you identified. Each card
gives: how to detect it, which summary statistics are valid, which tests to use,
the standard transform, and what it means for A/B testing.

## Identification Flowchart

Work top to bottom with the Step 2 diagnostics in hand:

1. **Discrete or continuous?** Integer-valued with a modest number of unique values
   is discrete (counts, successes); otherwise treat as continuous.
2. **Many exact zeros (>10% of values) on a count or spend column?** Suspect a
   zero-inflated distribution: model the zero process separately (see Zero-inflated
   card), then identify the positive part with the rest of this flowchart.
3. **Discrete counts:** compute the variance-to-mean ratio (VMR).
   - VMR near 1 -> Poisson
   - VMR much greater than 1 (overdispersed) -> negative binomial
   - VMR less than 1 with a fixed number of trials -> binomial
   - Counts of trials until first success (heavily right-skewed, mode at 1) -> geometric
4. **Bounded in (0, 1)?** Rates, proportions, percentages per unit -> beta.
5. **Continuous and positive only:**
   - Is log(x) approximately normal (Shapiro on log, Q-Q on log)? -> log-normal
   - Constant hazard / memoryless waiting times, sd roughly equal to mean -> exponential
   - Sum of several exponential-ish waits, right-skewed but not extreme -> gamma
   - Extremely heavy tail: mean/median ratio > 3, top 1% holds a large share of the
     total, straight line on a log-log survival plot -> power law / Pareto
6. **Symmetric, mean close to median, passes normality tests?** -> normal.
7. **Two humps (dip test significant, bimodality coefficient > 0.555)?** -> bimodal /
   mixture. Do not fit a single family; find the mixing variable.
8. **Flat between two bounds, no interior mode?** -> uniform (often a sign of
   synthetic data, rounding, or an ID column masquerading as a metric).

If tests disagree or nothing fits cleanly, say so: report the two or three closest
candidates with the evidence for each, use rank-based or bootstrap methods, and mark
confidence LOW. Never force a family onto data that does not fit one.

## Distribution cards

### Normal
- **Detect:** symmetric, mean close to median (ratio near 1), skewness near 0, excess
  kurtosis near 0, Shapiro-Wilk / Anderson-Darling not rejected, straight Q-Q line.
- **Valid stats:** mean, sd, standard confidence intervals. Median optional.
- **Tests:** t-test / Welch's t-test for two groups, ANOVA for several, Pearson
  correlation, OLS regression.
- **Transform:** none needed.
- **A/B:** the friendly case. Standard power analysis applies; mean difference with a
  t-test is fine at reasonable n.

### Log-normal
- **Detect:** positive only, right-skewed, log(x) passes normality checks. Common for
  revenue per order, session duration, latency.
- **Valid stats:** median and geometric mean; report the mean only alongside the
  median. IQR over sd.
- **Tests:** t-test on log(x) (compares geometric means), or Mann-Whitney U on raw
  values. Regression on log(x) gives multiplicative effects.
- **Transform:** log. Back-transform effect estimates as percent changes.
- **A/B:** raw-mean t-tests are noisy and outlier-dominated; test on log values or
  use bootstrapped difference in means. State whether the decision metric is the
  mean (total revenue) or the median (typical user) BEFORE running.

### Exponential
- **Detect:** positive, mode at zero, sd approximately equal to mean (CV near 1),
  memoryless waiting times (time between events).
- **Valid stats:** median and rate (1/mean); the mean is fine but skewed.
- **Tests:** rate comparison via Poisson/negative-binomial count models, or
  Mann-Whitney on waiting times; survival methods if censored.
- **Transform:** log for regression, or model as survival time.
- **A/B:** compare rates, not raw means; watch for censoring (users who have not
  converted YET are not failures).

### Gamma
- **Detect:** positive, right-skewed, less extreme than log-normal, CV below ~1.5;
  sums of waiting times, cost per account.
- **Valid stats:** mean with a gamma-appropriate CI, median, IQR.
- **Tests:** gamma GLM with log link for regression; Mann-Whitney or bootstrap for
  two groups.
- **Transform:** log usually adequate.
- **A/B:** gamma GLM or bootstrapped means. Behaves better than log-normal but the
  same mean-vs-median decision framing applies.

### Power law / Pareto (heavy tail)
- **Detect:** mean/median ratio > 3, top 1% of units holding tens of percent of the
  total, survival function straight on log-log axes, sd many times the mean. Whales:
  enterprise accounts, viral posts, big basket orders.
- **Valid stats:** median, percentiles (p90/p99), top-k share. The mean exists but is
  dominated by a handful of observations; the sd is close to meaningless.
- **Tests:** rank-based (Mann-Whitney), bootstrapped or winsorized/trimmed means,
  quantile regression.
- **Transform:** log helps but often stays non-normal; winsorize for mean-based
  reporting and SAY SO.
- **A/B:** the dangerous case. One whale can flip a raw-mean test; n requirements
  explode. Use winsorized means, CUPED, or rank tests, pre-register the cap, and
  report the tail separately (whale count per arm).

### Poisson
- **Detect:** discrete counts per fixed window, VMR near 1, events independent.
- **Valid stats:** mean (= variance), rate per exposure.
- **Tests:** Poisson rate test / Poisson GLM; chi-square for count tables.
- **Transform:** square root (legacy) or model directly with a GLM.
- **A/B:** compare rates with exposure offsets. Check VMR first: real product data is
  usually overdispersed, and a Poisson test on overdispersed data is overconfident.

### Negative binomial
- **Detect:** counts with VMR well above 1 (overdispersion): events per user where
  users differ in underlying rate (sessions, tickets, orders per customer).
- **Valid stats:** mean plus a dispersion parameter; median for the typical unit.
- **Tests:** negative binomial GLM; quasi-Poisson as a fallback.
- **Transform:** none; model it directly.
- **A/B:** use NB regression or a bootstrap over users. A Poisson assumption here
  understates the variance and produces false positives.

### Binomial
- **Detect:** k successes out of n trials per unit; conversion flags aggregate to
  binomial counts.
- **Valid stats:** proportion with a Wilson or Jeffreys interval (not the normal
  approximation at small n or extreme p).
- **Tests:** two-proportion z-test, chi-square, Fisher's exact at small n; logistic
  regression with covariates.
- **Transform:** logit for modeling.
- **A/B:** the standard conversion-rate case. Power analysis on proportions; check
  sample ratio (SRM) before reading the result.

### Geometric
- **Detect:** trials until first success; discrete, mode at 1, long right tail
  (attempts before conversion, contacts before reply).
- **Valid stats:** median attempts, success probability p.
- **Tests:** compare p via the binomial machinery on per-trial outcomes, or survival
  methods on trial counts.
- **Transform:** none; model per-trial probability.
- **A/B:** frame as per-trial conversion; censor units still in progress.

### Beta
- **Detect:** continuous values bounded in (0, 1): per-user rates, shares, utilization.
- **Valid stats:** mean and median both fine; report the bounds.
- **Tests:** beta regression; rank tests are a safe default. Do NOT t-test values
  piled up against 0 or 1.
- **Transform:** logit (after nudging exact 0/1 off the boundary), or model with
  zero-one-inflated beta when the boundary mass is real.
- **A/B:** if the underlying events are available, prefer the binomial machinery on
  raw events over t-tests on per-user ratios (ratio-of-averages vs average-of-ratios
  is a real decision; state which one the metric means).

### Uniform
- **Detect:** flat histogram between two bounds, no interior mode, Kolmogorov-Smirnov
  against uniform not rejected.
- **Valid stats:** min, max, midpoint.
- **Interpretation:** almost never a natural product metric. Suspect synthetic or
  simulated data, hash/ID columns, or heavy rounding. Investigate before analyzing.

### Bimodal / mixture
- **Detect:** two humps in the histogram/KDE, Hartigan dip test significant,
  bimodality coefficient > 0.555; Q-Q with a visible kink.
- **Valid stats:** none for the pooled column; every pooled summary (mean, median,
  sd) describes neither mode. Summarize per mode.
- **Method:** find the mixing variable (plan tier, platform, new-vs-returning) and
  split; or fit a 2-component mixture and report both components.
- **A/B:** test within segments, or the mix shift between arms will masquerade as a
  treatment effect (Simpson's paradox risk is highest here).

### Zero-inflated (counts or spend)
- **Detect:** a spike of exact zeros far above what the fitted count/continuous model
  predicts (many users never do the thing at all).
- **Valid stats:** report two numbers, never one: the participation rate (share
  non-zero) and the conditional intensity (mean/median among the non-zero).
- **Tests:** hurdle or zero-inflated models (ZIP/ZINB); or the simple two-part test:
  proportion test on participation plus a test on the positive part.
- **A/B:** a single test on the pooled column confounds "more users did it" with
  "the same users did more". Run the two-part analysis and say which part moved.

## Practical guidance

- **t-test robustness:** at n per arm in the thousands, the CLT covers moderate skew
  (roughly |skew| < 2-3) for mean comparisons; it does NOT cover power-law tails,
  bimodality, or zero-inflation. When in doubt, bootstrap the difference in means and
  compare against the t interval.
- **Family tree:** binomial -> Poisson (rare events, large n); Poisson + rate
  heterogeneity -> negative binomial; exponential summed -> gamma; many small
  multiplicative effects -> log-normal; preferential attachment -> power law.
- **Effect sizes:** report the difference in the decision-relevant statistic (mean,
  median, rate) with a CI, plus a standardized measure when comparing across metrics
  (Cohen's d for normal-ish, Cliff's delta or rank-biserial for skewed).
- **Censoring:** windowed metrics (7-day retention, time-to-convert) censor recent
  cohorts. Exclude units whose window has not closed, or use survival methods; never
  average complete and incomplete windows together.
