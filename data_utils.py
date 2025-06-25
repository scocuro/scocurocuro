import yfinance as yf

def fetch_last_close(ticker: str) -> float:
    df = yf.Ticker(ticker).history(period='5d')
    if df.empty:
        raise ValueError(f"No data for {ticker}")
    return float(df['Close'][-1])

def calc_decline_rate(close: float, strike: float) -> float:
    return (close - strike) / strike * 100
