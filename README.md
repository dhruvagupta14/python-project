# Python Technical Stock Screener
## Overview
#### This project is an automated stock screening tool designed to identify equity opportunities based on specific technical analysis criteria. It downloads historical market data for a predefined list of top S&P 500 companies, calculates key technical indicators, and filters stocks that meet a trend-following plus pullback strategy.
## Logic 
#### The screener applies the following five filters to identify stocks in a long-term uptrend that are currently experiencing a short-term pullback:
1. Long-Term Trend: Current Price > 200-Day Moving Average.

2. Intermediate Trend: Current Price > 150-Day Moving Average.

3. Golden Cross: 50-Day Moving Average > 200-Day Moving Average.

4. Momentum: Current Price is within 25% of the 52-Week High.

5. Entry Signal: Relative Strength Index (RSI) < 50 (indicating a pullback within the uptrend).

## Libraries Used
1. yfinance
2. pandas
3. numpy
4. datetime
