# CAPM

A small Python toolkit for fitting the Capital Asset Pricing Model (CAPM) to stock return data and visualizing the result as a Security Characteristic Line (SCL).

Given a market benchmark (e.g. SPY) and one or more assets, the tool downloads historical prices from Yahoo Finance, computes returns, regresses each asset's excess return against the market's excess return, and reports alpha, beta, R², and the asset's CAPM-implied expected return.

## Features

- Downloads historical price data directly from Yahoo Finance via `yfinance`
- Computes simple period-over-period returns from price series
- Fits CAPM via OLS regression on excess returns: `R_asset - Rf = alpha + beta * (R_market - Rf)`
- Reports beta, alpha, R², standard errors, t-statistics, and expected return for each asset
- Plots the Security Characteristic Line (asset returns vs. market returns) with the fitted regression line
- Simple command-line interface — no notebook or interactive setup required

## Project structure

```
CAPM/
├── main.py                  # CLI entry point
├── requirements.txt         # Python dependencies
├── src/
│   ├── fetcher.py           # Downloads prices from Yahoo Finance
│   ├── data_processor.py    # Loads/prepares price and return data
│   └── core_engine.py       # CAPM regression fitting and SCL plotting
├── data/                    # Downloaded price CSVs (created at runtime)
└── plots/                   # Output plots (created at runtime)
```

## Installation

Clone the repository and install dependencies, ideally inside a virtual environment:

```bash
git clone https://github.com/uctiot007/CAPM.git
cd CAPM
pip install -r requirements.txt
```

**Dependencies:** `pandas`, `numpy`, `matplotlib`, `scipy`, `statsmodels`, `yfinance`

> **Windows users:** if `python3` isn't recognized, use `python` instead. Make sure it points to a Python 3.x installation with the above packages installed.

## Usage

The CLI downloads price data for a set of tickers, fits CAPM for each asset against a chosen market benchmark, prints a summary, and saves a plot of the Security Characteristic Line for one selected asset.

### Basic example

```bash
python3 main.py --download SPY AAPL MSFT --market SPY --asset AAPL --save-plot plots/aapl_analysis.png
```

This downloads SPY, AAPL, and MSFT data for the last 365 days (the default window), uses SPY as the market benchmark, fits CAPM for AAPL, and saves a plot to `plots/aapl_analysis.png`.

### Full example with a custom date range

```bash
python3 main.py --download SPY AAPL MSFT --start 2020-01-01 --end 2023-01-01 --market SPY --asset AAPL --save-plot plots/aapl_vs_spy.png
```

### Arguments

| Flag | Description | Default |
|---|---|---|
| `--download` | Space-separated list of tickers to download (required) | — |
| `--start` | Start date, `YYYY-MM-DD` | 365 days before today |
| `--end` | End date, `YYYY-MM-DD` | today |
| `--interval` | Data interval: `1d`, `1wk`, or `1mo` | `1d` |
| `--market` | Ticker to use as the market benchmark | first ticker in `--download` |
| `--asset` | Ticker to plot against the market | first non-market ticker downloaded |
| `--save-plot` | Output path for the SCL plot | `CAPM/plots/capm_example.png` |
| `--prices` | Output path for the downloaded price CSV | `CAPM/data/prices.csv` |
| `--riskfree` | Risk-free rate per period, as a decimal | `0.0` |

### More examples

Use defaults for the time window (last 365 days):

```bash
python3 main.py --download TSLA MSFT GOOGL --market TSLA --asset MSFT --save-plot plots/msft_analysis.png
```

Analyze a specific calendar year:

```bash
python3 main.py --download SPY NVDA --start 2022-01-01 --end 2022-12-31 --market SPY --asset NVDA --save-plot plots/nvda_2022.png
```

> This tool only supports downloading data from Yahoo Finance; local CSV input and interactive prompts are not supported in the current version.

## How it works

1. **Fetch** — `src/fetcher.py` downloads adjusted close prices for the requested tickers over the chosen date range and interval, and saves them to a CSV.
2. **Process** — `src/data_processor.py` splits the price data into a market series and one or more asset series, and converts prices into period returns.
3. **Fit** — `src/core_engine.py` regresses each asset's excess return (return minus the risk-free rate) against the market's excess return using OLS, returning beta, alpha, R², standard errors, t-statistics, and the CAPM-implied expected return.
4. **Plot** — the same module renders a scatter plot of asset vs. market returns with the fitted Security Characteristic Line overlaid, annotated with alpha, beta, and R².

## Output

Running the CLI prints a per-asset summary table to the console (beta, alpha, R², standard error, expected return) and writes a PNG plot of the Security Characteristic Line for the selected asset to the path given by `--save-plot`.

## License

No license file is currently included in this repository.
