# CAPM
Capital Asset pricing model: 
=======
CAPM example package
=====================

This small package provides utilities to fit the Capital Asset Pricing Model (CAPM)
to asset return series and visualize the Security Characteristic Line (SCL).

Quick start
-----------

1. Install dependencies (recommended in a virtualenv):

```
pip install -r requirements.txt
pip install statsmodels
```

2. Run with stocks, timeframe, asset choice, and output file:

```
python3 CAPM/main.py --download SPY AAPL MSFT --start 2020-01-01 --end 2023-01-01 --market SPY --asset AAPL --save-plot CAPM/plots/aapl_analysis.png
```

**Breakdown:**
- `--download SPY AAPL MSFT`: Stock tickers to download
- `--start 2020-01-01 --end 2023-01-01`: Time frame (omit for last 365 days)
- `--market SPY`: Market benchmark
- `--asset AAPL`: Which asset to plot (omit for first asset)
- `--save-plot CAPM/plots/aapl_analysis.png`: Output file name

3. Use last 365 days (default):

```
python3 CAPM/main.py --download SPY AAPL MSFT --market SPY --asset MSFT --save-plot CAPM/plots/msft_recent.png
```

> This version only supports downloading data from Yahoo Finance. Local CSV and interactive input modes have been removed.

Windows compatibility note:
- If `python3` is not available on Windows, use `python` instead.
- Ensure `python` points to Python 3.x and that `yfinance` and other dependencies are installed.

Download from Yahoo Finance
---------------------------

**Complete example with all parameters:**

```
python3 CAPM/main.py --download SPY AAPL MSFT --start 2020-01-01 --end 2023-01-01 --market SPY --asset AAPL --save-plot CAPM/plots/aapl_vs_spy.png
```

**Using defaults (last 365 days):**

```
python3 CAPM/main.py --download TSLA MSFT GOOGL --market TSLA --asset MSFT --save-plot CAPM/plots/msft_analysis.png
```

**Different date ranges:**

```
# Last 2 years
python3 CAPM/main.py --download AAPL MSFT --start 2024-06-17 --end 2026-06-17 --market AAPL --asset MSFT --save-plot CAPM/plots/msft_2yr.png

# Specific year
python3 CAPM/main.py --download SPY NVDA --start 2022-01-01 --end 2022-12-31 --market SPY --asset NVDA --save-plot CAPM/plots/nvda_2022.png
```



Files of interest
- `src/core_engine.py`: CAPM fitting and plotting helpers
- `src/data_processor.py`: CSV loading and return computation
- `main.py`: simple CLI runner and example

