import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_moving_average(data, window):
    """
    Calculate moving average for given data and window period
    
    Args:
        data (pandas.Series): Price data
        window (int): Number of periods for moving average
    
    Returns:
        pandas.Series: Moving average values
    """
    return data.rolling(window=window).mean()

def calculate_rsi(data, window=14):
    """
    Calculate Relative Strength Index (RSI)
    
    Args:
        data (pandas.Series): Price data
        window (int): Period for RSI calculation (default 14)
    
    Returns:
        pandas.Series: RSI values
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_top_sp500_tickers():
    """
    Return a predefined list of top S&P 500 tickers.
    In a real application, you might fetch this dynamically from a source like Wikipedia.
    
    Returns:
        list: List of top S&P 500 ticker symbols
    """
    # This is a sample list of top S&P 500 companies by market cap as of early 2026

    sp500_tickers = [
        'MSFT', 'AAPL', 'AMZN', 'NVDA', 'GOOGL', 'TSLA', 'META', 'BRK-B', 'JPM',
        'JNJ', 'V', 'WMT', 'PG', 'MA', 'HD', 'DIS', 'PYPL', 'BAC', 'ADBE', 'NFLX',
        'CRM', 'CSCO', 'XOM', 'VZ', 'KO', 'PFE', 'MRK', 'T', 'PEP', 'ABT', 'ABBV',
        'AVGO', 'CVX', 'LLY', 'COST', 'TMUS', 'DHR', 'ACN', 'QCOM', 'TXN', 'NEE',
        'LIN', 'HON', 'UNH', 'WFC', 'GS', 'BA', 'CAT', 'INTC', 'RTX'
    ]
    return sp500_tickers

def screen_stocks(tickers, period="3y"):
    """
    Screen stocks based on technical criteria
    
    Args:
        tickers (list): List of stock ticker symbols
        period (str): Time period for historical data (default "3y")
    
    Returns:
        pandas.DataFrame: DataFrame containing screened stocks
    """
    results = []
    
    for ticker in tickers:
        try:
            # Download historical data for the ticker
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            # Check if we have enough data
            if len(hist) < 200:
                print(f"Insufficient data for {ticker}, skipping...")
                continue
            
            # Calculate required indicators
            hist['MA_50'] = calculate_moving_average(hist['Close'], 50)
            hist['MA_150'] = calculate_moving_average(hist['Close'], 150)
            hist['MA_200'] = calculate_moving_average(hist['Close'], 200)
            hist['RSI'] = calculate_rsi(hist['Close'],14)

            
            # Get the latest values
            current_price = hist['Close'].iloc[-1]
            ma_50 = hist['MA_50'].iloc[-1]
            ma_150 = hist['MA_150'].iloc[-1]
            ma_200 = hist['MA_200'].iloc[-1]
            rsi = hist['RSI'].iloc[-1]
            
            # Calculate 52-week high
            fifty_two_week_high = hist['High'].rolling(252).max().iloc[-1]
            
            # Check screening criteria
            price_above_ma200 = current_price > ma_200  # Current Price > 200-day MA
            price_above_ma150 = current_price > ma_150  # Current Price > 150-day MA
            golden_cross = ma_50 > ma_200  # Golden Cross condition
            near_52week_high = current_price >= 0.75 * fifty_two_week_high  # Within 25% of 52-week high
            rsi_under_50 = rsi < 50  # RSI < 50 (pullback in uptrend)
            
            # Apply all filters
            if all([
                price_above_ma200,
                price_above_ma150,
                golden_cross,
                near_52week_high,
                rsi_under_50
            ]):
                results.append({
                    'Ticker': ticker,
                    'Current_Price': round(current_price, 2),
                    'MA_50': round(ma_50, 2),
                    'MA_150': round(ma_150, 2),
                    'MA_200': round(ma_200, 2),
                    'RSI': round(rsi, 2),
                    '52_Week_High': round(fifty_two_week_high, 2),
                    'Price_to_52W_High_Pct': round((current_price / fifty_two_week_high) * 100, 2)
                })
                
        except Exception as e:
            print(f"Error processing {ticker}: {str(e)}")
            continue
    
    # Create DataFrame with results
    df_results = pd.DataFrame(results)
    
    return df_results

def main():
    """
    Main function to run the stock screening process
    """
    print("Starting Stock Screening Process...")
    
    # Get the list of tickers to screen
    tickers = get_top_sp500_tickers()
    
    # Screen the stocks based on criteria
    screened_stocks = screen_stocks(tickers)
    
    # Display results
    if not screened_stocks.empty:
        print("\nScreened Stocks Summary:")
        print("="*80)
        print(screened_stocks.to_string(index=False))
        
        # Export to CSV file
        filename = "screened_stocks.csv"
        screened_stocks.to_csv(filename, index=False)
        print(f"\nResults exported to {filename}")
    else:
        print("\nNo stocks met all screening criteria.")
    
    print(f"\nScreening completed at {datetime.now()}")

if __name__ == "__main__":
    main()