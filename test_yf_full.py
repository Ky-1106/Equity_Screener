import yfinance as yf
import time

symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS", "WIPRO.NS", "ASIANPAINT.NS"]

start = time.time()

# 1. Fetch 5y weekly history for all symbols in one go
hist_data = yf.download(symbols, period="5y", interval="1wk")
print(f"History time: {time.time() - start:.2f}s")
start = time.time()

# 2. Fetch fundamental info for all symbols
tickers = yf.Tickers(" ".join(symbols))
fundamentals = {}
for sym in symbols:
    info = tickers.tickers[sym].info
    fundamentals[sym] = {
        "pe": info.get("trailingPE"),
        "mc": info.get("marketCap"),
        "roe": info.get("returnOnEquity"),
        "div": info.get("dividendYield")
    }

print(f"Info time: {time.time() - start:.2f}s")
print(fundamentals["RELIANCE.NS"])
