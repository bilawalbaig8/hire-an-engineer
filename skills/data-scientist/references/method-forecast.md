# Method: Forecast mode

When to read this: any number about future periods (installs, revenue, DAU, demand). Code for a backtest and simple intervals is in `stdlib-helpers.md`.

## 1. Steps

1. **Frame**: what decision uses the forecast (a budget, hiring, server capacity), the horizon, the unit (per day, per month), and the cost of being too high versus too low. The cost tells you whether to plan on the central value or on a cautious one.
2. **Audit the history**: length, gaps, changes in definition, one-off events (store features, outages, campaigns) from notes next to the data. Plot it as text (one line per period) and read it.
3. **Handle one-offs**: a feature, outage or launch spike is removed or capped for fitting (say which and why) and not projected forward unless it will repeat.
4. **Baselines first** (the forecast must beat these on a backtest):
   - naive: next = last value;
   - mean of the last k periods;
   - drift: last value plus the average change;
   - seasonal naive: same period last cycle (only when at least two full cycles exist).
   Simple methods and combinations often match or beat complex ones [S-FOR-3]; the standard open text covers these baselines and accuracy measures (S-FOR-1, unverified).
5. **Backtest**: hold out the last few periods (at least the forecast horizon), forecast them from the earlier data, measure the error (mean absolute error, and percentage error when the scale is stable). Use rolling origins when the series allows [S-MOD-13].
6. **Choose** the simplest method with the best backtest. More complex models (exponential smoothing, ARIMA, additive trend and seasonality models) only when there is enough history and the library is installed [S-FOR-4] [S-FOR-2].
7. **Intervals**: from the backtest errors or from the spread of period-to-period changes; they widen with the horizon (for a random-walk-like series, roughly with the square root of the number of steps ahead). Give 80% and 95% ranges.
8. **Report**: a table with central value, 80% and 95% ranges per period; the method and the baseline it beat; what is not in the model (seasonality not estimable, planned campaigns, price changes); the one or two things that would move it most.

## 2. Short series and seasonality

- With less than two full cycles (for monthly data, under 24 months), a yearly pattern cannot be estimated. Say so plainly: "a December holiday effect is possible but this data cannot show it".
- With very few points (under about 12), keep to naive, mean or drift and wide intervals.

## 3. When the owner wants "one exact number"

Give one number and its range in the same sentence, and a planning recommendation tied to the decision: "Plan on about 5,000 a week; with 80% confidence it falls between 4,300 and 5,700; if running short is costly, budget for the low end". A single number without a range invites planning on luck; refusing to give any number is also unhelpful [S-COM-5].

## 4. Common failure modes

- Fitting a trend through a one-off spike.
- Reporting in-sample fit as accuracy.
- Seasonal models on one cycle of data.
- Intervals that do not widen with the horizon.
- Forecasting a ratio (revenue per user) and a count (users) separately and multiplying without carrying both uncertainties.
- Ignoring known future changes the owner mentioned (a campaign, a price change): list them as outside the model.
