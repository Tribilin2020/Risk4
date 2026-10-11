import logging
import sys

import pandas as pd
import yfinance as yf

# ******************************************************************************
#   INPUT YOUR DATA HERE
#
#   PORTFOLIO_VALUE   total value of your portfolio
#   PORTFOLIO         your stocks as "TICKER": percentage of the portfolio
#                     (the percentages must add up to 100)
#   MARKET_TICKER     ticker that represents the market move, e.g. "NVDA"
#   MARKET_MOVE       move you want to simulate for that ticker, in %, e.g. -30
#   WINDOW            7 or 30 -> number of trading days used to calculate the betas
# ******************************************************************************
# INPUT DATA HERE:

PORTFOLIO_VALUE = 100_000

PORTFOLIO = {
    "SMH": 1,
    "MU": 1,
    "NVDA": 97,
    "AAPL": 1,
}

MARKET_TICKER = "NVDA"
MARKET_MOVE = -30

WINDOW = 30
# ******************************************************************************

logging.getLogger("yfinance").setLevel(logging.CRITICAL)


def stop(message):
    print(message)
    sys.exit(1)


holdings = {t.strip().upper(): w for t, w in PORTFOLIO.items()}
market = MARKET_TICKER.strip().upper()

if WINDOW not in (7, 30):
    stop("WINDOW must be 7 or 30.")

if abs(sum(holdings.values()) - 100) > 0.01:
    stop(f"Portfolio percentages add up to {sum(holdings.values())}, they must add up to 100.")

tickers = sorted(set(holdings) | {market})

data = yf.download(tickers, period="6mo", auto_adjust=True, progress=False)
if data.empty:
    stop("Could not download any price data. Check the tickers and your internet connection.")

prices = data["Close"]
if isinstance(prices, pd.Series):
    prices = prices.to_frame(tickers[0])

for t in tickers:
    if t not in prices.columns or prices[t].dropna().empty:
        stop(f"Ticker not recognized: {t}")

returns = prices[tickers].pct_change(fill_method=None).dropna().tail(WINDOW)

if len(returns) < WINDOW:
    stop("Not enough price history to calculate the betas.")

market_returns = returns[market]

rows = []
for t, w in holdings.items():
    beta = returns[t].cov(market_returns) / market_returns.var()
    move = max(beta * MARKET_MOVE / 100, -1.0)
    change = PORTFOLIO_VALUE * w / 100 * move
    rows.append((t, w, beta, move, change))

total_change = sum(r[4] for r in rows)

line = "*" * 70
print()
print(line)
print("YOUR RESULT")
print(f"Expected move of your portfolio if {market} moves {MARKET_MOVE:+.1f}%,")
print(f"based on the {WINDOW}-day beta of each stock to {market}.")
print(line)
print()
print(f"{'Ticker':<8}{'Weight':>9}{'Beta':>8}{'Exp. move':>12}{'Value change':>16}")
for t, w, beta, move, change in rows:
    print(f"{t:<8}{w:>8.1f}%{beta:>8.2f}{move * 100:>11.1f}%{change:>16,.2f}")
print()
print(f"Portfolio value before: {PORTFOLIO_VALUE:>16,.2f}")
print(f"Portfolio value after:  {PORTFOLIO_VALUE + total_change:>16,.2f}")
print(f"Expected change:        {total_change:>16,.2f}  ({total_change / PORTFOLIO_VALUE * 100:+.2f}%)")

if WINDOW == 7:
    print()
    print("Note: 7-day betas use only 7 daily returns, treat them as a rough estimate.")
print()
