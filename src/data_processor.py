"""Data loading and processing utilities for CAPM examples.

Functions:
- load_prices_csv: load a CSV of prices and return a DataFrame
- compute_returns: compute simple returns (period-over-period percentage change)
- prepare_market_and_assets: split market column and asset columns, return returns series/dataframe
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def load_prices_csv(path: str, date_col: str = "Date", parse_dates: bool = True) -> pd.DataFrame:
	"""Load a CSV file of prices into a DataFrame indexed by date."""
	df = pd.read_csv(path, parse_dates=[date_col] if parse_dates else None)
	if date_col in df.columns:
		df = df.set_index(date_col).sort_index()
	return df


def compute_returns(prices: pd.DataFrame, log: bool = False) -> pd.DataFrame:
	"""Compute period returns from price series.

	By default computes simple returns: pct_change.
	If `log` is True, computes log returns: diff(log(price)).
	"""
	if log:
		return np.log(prices).diff().dropna()
	return prices.pct_change().dropna()


def prepare_market_and_assets(prices: pd.DataFrame, market_col: str) -> tuple[pd.Series, pd.DataFrame]:
	"""Given a prices DataFrame, compute returns and split market vs asset returns.

	Returns (market_returns, assets_returns_df)
	"""
	returns = compute_returns(prices)
	if market_col not in returns.columns:
		raise KeyError(f"market_col '{market_col}' not found in price columns")
	market = returns[market_col]
	assets = returns.drop(columns=[market_col])
	return market, assets

