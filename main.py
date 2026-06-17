"""CAPM CLI using only Yahoo Finance data.

This script downloads ticker data from Yahoo Finance, computes CAPM statistics,
plots the chosen asset versus the selected market, and saves the result.
"""
from __future__ import annotations

import argparse
import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt

from src import core_engine, data_processor
from src import fetcher


def main():
	default_end = datetime.now().strftime("%Y-%m-%d")
	default_start = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

	parser = argparse.ArgumentParser(description="Run CAPM fits from Yahoo Finance price data")
	parser.add_argument("--download", nargs="+", required=True, help="Tickers to download from Yahoo Finance")
	parser.add_argument("--start", default=default_start, help=f"Start date (YYYY-MM-DD). Default: {default_start}")
	parser.add_argument("--end", default=default_end, help=f"End date (YYYY-MM-DD). Default: {default_end}")
	parser.add_argument("--interval", default="1d", help="Data interval: 1d, 1wk, 1mo")
	parser.add_argument("--market", help="Market benchmark ticker (default: first downloaded ticker)")
	parser.add_argument("--asset", help="Asset ticker to plot (default: first non-market asset)")
	parser.add_argument("--save-plot", default="CAPM/plots/capm_example.png", help="Path for output plot")
	parser.add_argument("--prices", default="CAPM/data/prices.csv", help="Path to save downloaded CSV")
	parser.add_argument("--riskfree", type=float, default=0.0, help="Risk-free rate per period (decimal)")
	args = parser.parse_args()

	market_col = args.market or args.download[0]
	print(f"Downloading {args.download} from {args.start} to {args.end}...")
	os.makedirs(os.path.dirname(args.prices), exist_ok=True)
	prices = fetcher.fetch_and_save(args.download, args.prices, start=args.start, end=args.end, interval=args.interval)
	print(f"Saved downloaded data to {args.prices}")

	if market_col not in prices.columns:
		print(f"Market ticker '{market_col}' not found in downloaded data. Using '{args.download[0]}' instead.")
		market_col = args.download[0]

	market, assets = data_processor.prepare_market_and_assets(prices, market_col)
	summary = core_engine.fit_capm_panel(assets, market, risk_free_rate=args.riskfree)
	print(summary)

	plot_asset = args.asset or next((ticker for ticker in assets.columns if ticker != market_col), assets.columns[0])
	if plot_asset not in assets.columns:
		available = ", ".join(assets.columns.tolist())
		raise ValueError(f"Asset '{plot_asset}' not found in downloaded data. Available: {available}")

	res = core_engine.fit_capm(assets[plot_asset], market, risk_free_rate=args.riskfree)
	core_engine.plot_scl(market, assets[plot_asset], fit_results=res, title=f"SCL: {plot_asset}")

	os.makedirs(os.path.dirname(args.save_plot), exist_ok=True)
	plt.savefig(args.save_plot, bbox_inches="tight")
	plt.close()
	print(f"Saved plot to {args.save_plot}")


if __name__ == "__main__":
	main()

