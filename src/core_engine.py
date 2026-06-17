"""CAPM modelling utilities.

This module provides functions to fit the Capital Asset Pricing Model (CAPM),
apply it across a panel of assets, compute expected returns from beta, and
plot the Security Characteristic Line (SCL).
"""
from __future__ import annotations

import typing as t

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


def _ensure_series(x) -> pd.Series:
	if isinstance(x, pd.Series):
		return x.dropna()
	return pd.Series(x).dropna()


def fit_capm(
	asset_returns: t.Union[pd.Series, np.ndarray],
	market_returns: t.Union[pd.Series, np.ndarray],
	risk_free_rate: float = 0.0,
) -> dict:
	"""Fit a CAPM regression and return results.

	The regression is performed on excess returns: (R_asset - Rf) ~ alpha + beta*(R_market - Rf).

	Returns a dictionary with fitted parameters, statistics, and the statsmodels `model`.
	"""
	y = _ensure_series(asset_returns)
	x = _ensure_series(market_returns)

	# align indexes
	df = pd.concat([y, x], axis=1, join="inner")
	df.columns = ["asset", "market"]
	if df.empty:
		raise ValueError("No overlapping observations between asset and market returns")

	# excess returns
	df["asset_excess"] = df["asset"] - risk_free_rate
	df["market_excess"] = df["market"] - risk_free_rate

	X = sm.add_constant(df["market_excess"])  # intercept = alpha
	model = sm.OLS(df["asset_excess"], X).fit()

	beta = float(model.params["market_excess"])
	alpha = float(model.params["const"])

	mean_asset = float(df["asset"].mean())
	mean_market = float(df["market"].mean())
	market_premium = mean_market - risk_free_rate
	expected_return = risk_free_rate + beta * market_premium

	return {
		"beta": beta,
		"alpha": alpha,
		"r2": float(model.rsquared),
		"stderr_beta": float(model.bse["market_excess"]),
		"stderr_alpha": float(model.bse["const"]),
		"t_beta": float(model.tvalues["market_excess"]),
		"t_alpha": float(model.tvalues["const"]),
		"pvalues": model.pvalues.to_dict(),
		"residuals": model.resid,
		"fitted_excess": model.fittedvalues,
		"fittedvalues_raw": model.fittedvalues + risk_free_rate,
		"mean_asset_return": mean_asset,
		"mean_market_return": mean_market,
		"expected_return": expected_return,
		"risk_free_rate": risk_free_rate,
		"model": model,
	}


def fit_capm_panel(
	returns_df: pd.DataFrame,
	market: pd.Series,
	risk_free_rate: float = 0.0,
) -> pd.DataFrame:
	"""Fit CAPM for each column in `returns_df` (columns are asset return series).

	Returns a DataFrame summarizing beta, alpha, r2, stderr_beta, expected_return.
	"""
	results = []
	for col in returns_df.columns:
		try:
			res = fit_capm(returns_df[col], market, risk_free_rate=risk_free_rate)
			results.append(
				{
					"asset": col,
					"beta": res["beta"],
					"alpha": res["alpha"],
					"r2": res["r2"],
					"stderr_beta": res["stderr_beta"],
					"expected_return": res["expected_return"],
				}
			)
		except Exception:
			results.append({"asset": col, "beta": np.nan, "alpha": np.nan, "r2": np.nan})

	return pd.DataFrame(results).set_index("asset")


def expected_return(beta: float, mean_market_return: float, risk_free_rate: float = 0.0) -> float:
	"""Compute expected CAPM return: Rf + beta * (E[Rm] - Rf)"""
	return risk_free_rate + beta * (mean_market_return - risk_free_rate)


def plot_scl(
	market_returns: t.Union[pd.Series, np.ndarray],
	asset_returns: t.Union[pd.Series, np.ndarray],
	fit_results: dict | None = None,
	ax: plt.Axes | None = None,
	title: str | None = None,
) -> plt.Axes:
	"""Plot Security Characteristic Line (asset returns vs market returns).

	If `fit_results` is a dict returned by `fit_capm`, the regression line will be plotted
	on raw returns by converting the excess-return regression back to raw-return form:

		R_asset = Rf + alpha + beta * (R_market - Rf)

	"""
	y = _ensure_series(asset_returns)
	x = _ensure_series(market_returns)
	df = pd.concat([x, y], axis=1, join="inner")
	df.columns = ["market", "asset"]

	if ax is None:
		fig, ax = plt.subplots(figsize=(7, 5))

	ax.scatter(df["market"], df["asset"], alpha=0.6)

	if fit_results is not None:
		beta = fit_results.get("beta")
		alpha = fit_results.get("alpha")
		rf = fit_results.get("risk_free_rate", 0.0)

		xl = np.linspace(df["market"].min(), df["market"].max(), 200)
		yl = rf + alpha + beta * (xl - rf)
		ax.plot(xl, yl, color="C1", lw=2, label=f"SCL (beta={beta:.3f})")
		ax.legend()
		ax.annotate(
			f"alpha={alpha:.4f}\nbeta={beta:.4f}\nr2={fit_results.get('r2'):.3f}",
			xy=(0.02, 0.98),
			xycoords="axes fraction",
			va="top",
		)

	ax.set_xlabel("Market Return")
	ax.set_ylabel("Asset Return")
	if title:
		ax.set_title(title)

	return ax

