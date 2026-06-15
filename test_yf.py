import yfinance as yf
import json

symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS", "WIPRO.NS", "ASIANPAINT.NS"]
tickers = yf.Tickers(" ".join(symbols))

prices = {}
for sym in symbols:
    info = tickers.tickers[sym].fast_info
    # fast_info is a dictionary-like object that is MUCH faster to fetch than .info
    clean_sym = sym.replace(".NS", "")
    prices[clean_sym] = {
        "price": info.last_price,
        "change_pct": ((info.last_price - info.previous_close) / info.previous_close) * 100
    }

print(json.dumps(prices, indent=2))
