"""Simple Yahoo Finance fetcher helper using yfinance.

Functions:
- fetch_prices: download adjusted close prices for given tickers
- fetch_and_save: download and save CSV with Date column
"""
from __future__ import annotations

import typing as t
import pandas as pd


def fetch_prices(tickers: t.List[str], start: str | None = None, end: str | None = None, interval: str = "1d") -> pd.DataFrame:
    """Download adjusted close prices for tickers using yfinance.

    Returns a DataFrame indexed by date with columns equal to tickers.
    Requires `yfinance` to be installed.
    """
    try:
        import yfinance as yf
    except Exception as e:
        raise RuntimeError("yfinance is required to fetch prices; install it with pip install yfinance") from e

    data = yf.download(tickers, start=start, end=end, interval=interval, progress=False)
    
    # yfinance returns multi-level columns when downloading multiple tickers or when auto_adjust is used
    # Try to extract the Adj Close or Close prices
    if isinstance(data, pd.DataFrame):
        # Check for multi-level columns
        if isinstance(data.columns, pd.MultiIndex):
            # Multi-level: try Adj Close first, then Close
            if "Adj Close" in data.columns.get_level_values(0):
                prices = data["Adj Close"]
            elif "Close" in data.columns.get_level_values(0):
                prices = data["Close"]
            else:
                prices = data.iloc[:, 0:len(tickers)]  # Fallback: first N columns
        elif "Adj Close" in data.columns:
            prices = data["Adj Close"]
        elif "Close" in data.columns:
            prices = data["Close"]
        else:
            prices = data
    else:
        prices = data

    # If single ticker, ensure DataFrame
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    # Rename columns to ticker names if they're not already
    if len(prices.columns) == len(tickers):
        prices.columns = tickers
    
    prices = prices.dropna(how="all")
    prices.index.name = "Date"
    return prices


def fetch_and_save(tickers: t.List[str], path: str, start: str | None = None, end: str | None = None, interval: str = "1d") -> pd.DataFrame:
    prices = fetch_prices(tickers, start=start, end=end, interval=interval)
    df = prices.reset_index()
    df.to_csv(path, index=False)
    return prices
