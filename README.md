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

## Project Structure
-calculate_moving_average(): Computes rolling moving averages.

-calculate_rsi(): Computes the Relative Strength Index.

-get_top_sp500_tickers(): Returns the universe of stocks to screen.

-screen_stocks(): Main logic loop that downloads data, applies filters, and handles errors.

-main(): Entry point for execution.

## Output 
Console: A summarized DataFrame of stocks meeting all criteria.
File: A detailed report saved as screened_stocks.csv containing:
1.Ticker Symbol

2.Current Price

3.Moving Averages (50, 150, 200 Day)

4.RSI Value

5.52-Week High

6.Percentage of Price relative to 52-Week High
