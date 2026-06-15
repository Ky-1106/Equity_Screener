import yfinance as yf
import time
import threading
from threading import Lock

# Expanded Nifty 50 Universe
STATIC_STOCKS = [
    # Finance
    {"t": "HDFCBANK", "n": "HDFC Bank Ltd", "sec": "Finance", "ind": "Private Banking", "rat": "Strong Buy", "tgt": 2050, "pros": ["Largest private sector bank", "Excellent asset quality"], "cons": ["High credit-deposit ratio"]},
    {"t": "ICICIBANK", "n": "ICICI Bank Ltd", "sec": "Finance", "ind": "Private Banking", "rat": "Strong Buy", "tgt": 1500, "pros": ["Remarkable ROE expansion", "Strong retail loan growth"], "cons": ["Unsecured loan growth risks"]},
    {"t": "SBIN", "n": "State Bank of India", "sec": "Finance", "ind": "Public Banking", "rat": "Buy", "tgt": 950, "pros": ["Largest branch network in India", "Improving asset quality"], "cons": ["PSU inefficiencies"]},
    {"t": "AXISBANK", "n": "Axis Bank Ltd", "sec": "Finance", "ind": "Private Banking", "rat": "Buy", "tgt": 1350, "pros": ["Citi acquisition synergies", "Strong corporate book"], "cons": ["Deposit growth lagging"]},
    {"t": "KOTAKBANK", "n": "Kotak Mahindra Bank", "sec": "Finance", "ind": "Private Banking", "rat": "Hold", "tgt": 1900, "pros": ["Premium valuation historically", "Strong margins"], "cons": ["RBI restrictions on digital onboarding"]},
    {"t": "BAJFINANCE", "n": "Bajaj Finance Ltd", "sec": "Finance", "ind": "NBFC", "rat": "Hold", "tgt": 8000, "pros": ["Dominant in consumer durables financing", "High ROA"], "cons": ["Rising cost of funds", "Asset quality concerns in rural"]},
    
    # Technology
    {"t": "TCS", "n": "Tata Consultancy Services", "sec": "Technology", "ind": "IT Services", "rat": "Buy", "tgt": 4100, "pros": ["Industry-leading margins", "Strong client retention"], "cons": ["Macro headwinds in US/EU"]},
    {"t": "INFY", "n": "Infosys Ltd", "sec": "Technology", "ind": "IT Services", "rat": "Buy", "tgt": 1900, "pros": ["Strong deal wins", "High dividend payout"], "cons": ["Margin pressure vs TCS"]},
    {"t": "WIPRO", "n": "Wipro Ltd", "sec": "Technology", "ind": "IT Services", "rat": "Hold", "tgt": 550, "pros": ["Cheaper valuation", "Turnaround efforts underway"], "cons": ["Market share losses"]},
    {"t": "HCLTECH", "n": "HCL Technologies", "sec": "Technology", "ind": "IT Services", "rat": "Buy", "tgt": 1800, "pros": ["Strong ER&D segment", "Software products division"], "cons": ["Seasonal weakness in products"]},
    {"t": "TECHM", "n": "Tech Mahindra", "sec": "Technology", "ind": "IT Services", "rat": "Hold", "tgt": 1400, "pros": ["Telecom vertical leadership", "New CEO turnaround"], "cons": ["Telecom capex slowdown"]},

    # Energy
    {"t": "RELIANCE", "n": "Reliance Industries", "sec": "Energy", "ind": "Conglomerate", "rat": "Strong Buy", "tgt": 3400, "pros": ["Jio & Retail dominance", "New Energy transition"], "cons": ["High capex debt"]},
    {"t": "ONGC", "n": "Oil & Natural Gas Corp", "sec": "Energy", "ind": "Oil & Gas", "rat": "Hold", "tgt": 300, "pros": ["High dividend yield", "Monetization of new blocks"], "cons": ["Windfall tax risks", "Aging fields"]},
    {"t": "NTPC", "n": "NTPC Ltd", "sec": "Energy", "ind": "Power Generation", "rat": "Buy", "tgt": 400, "pros": ["Aggressive renewable expansion", "Regulated assured returns"], "cons": ["ESG concerns on coal assets"]},
    {"t": "POWERGRID", "n": "Power Grid Corp", "sec": "Energy", "ind": "Power Transmission", "rat": "Buy", "tgt": 320, "pros": ["Monopoly in transmission", "Consistent high dividends"], "cons": ["Lower growth phase"]},

    # Consumer
    {"t": "ITC", "n": "ITC Ltd", "sec": "Consumer", "ind": "FMCG & Cigarettes", "rat": "Buy", "tgt": 510, "pros": ["Exceptional cash flow", "FMCG margin expansion"], "cons": ["Tobacco tax risks"]},
    {"t": "HINDUNILVR", "n": "Hindustan Unilever", "sec": "Consumer", "ind": "FMCG", "rat": "Hold", "tgt": 2600, "pros": ["Unmatched distribution", "Market leader across categories"], "cons": ["Rural demand slowdown", "High valuation"]},
    {"t": "ASIANPAINT", "n": "Asian Paints", "sec": "Consumer", "ind": "Paints", "rat": "Hold", "tgt": 3200, "pros": ["50%+ market share", "Asset-light model"], "cons": ["Grasim entry heightens competition"]},
    {"t": "TITAN", "n": "Titan Company", "sec": "Consumer", "ind": "Luxury", "rat": "Buy", "tgt": 4000, "pros": ["Jewelry formalization tailwind", "Strong brand equity"], "cons": ["Gold price volatility"]},
    {"t": "NESTLEIND", "n": "Nestle India", "sec": "Consumer", "ind": "FMCG", "rat": "Hold", "tgt": 2800, "pros": ["Pricing power", "Rural penetration increasing"], "cons": ["Very expensive valuation"]},
    {"t": "BRITANNIA", "n": "Britannia Industries", "sec": "Consumer", "ind": "FMCG", "rat": "Buy", "tgt": 5500, "pros": ["Market leader in biscuits", "Improving distribution"], "cons": ["Wheat and sugar inflation"]},

    # Automobile
    {"t": "MARUTI", "n": "Maruti Suzuki", "sec": "Automobile", "ind": "Auto Maker", "rat": "Buy", "tgt": 14000, "pros": ["Dominant market share", "Strong hybrid lineup"], "cons": ["Late to pure EV transition"]},
    {"t": "M&M", "n": "Mahindra & Mahindra", "sec": "Automobile", "ind": "Auto Maker", "rat": "Buy", "tgt": 2400, "pros": ["SUV market leadership", "Strong tractor cycle"], "cons": ["Capital allocation concerns"]},
    {"t": "BAJAJ-AUTO", "n": "Bajaj Auto", "sec": "Automobile", "ind": "Two Wheelers", "rat": "Hold", "tgt": 9000, "pros": ["Strong exports", "High margins"], "cons": ["Domestic market share loss"]},
    {"t": "HEROMOTOCO", "n": "Hero MotoCorp", "sec": "Automobile", "ind": "Two Wheelers", "rat": "Hold", "tgt": 4500, "pros": ["Rural market leader", "High dividend"], "cons": ["Weak premium portfolio"]},

    # Pharma
    {"t": "SUNPHARMA", "n": "Sun Pharma", "sec": "Pharma", "ind": "Pharmaceuticals", "rat": "Buy", "tgt": 1600, "pros": ["Specialty portfolio growth", "India business strong"], "cons": ["US FDA scrutiny"]},
    {"t": "DRREDDY", "n": "Dr. Reddy's Labs", "sec": "Pharma", "ind": "Pharmaceuticals", "rat": "Buy", "tgt": 6500, "pros": ["Strong US generic pipeline", "Healthy balance sheet"], "cons": ["Pricing pressure in US"]},
    {"t": "CIPLA", "n": "Cipla Ltd", "sec": "Pharma", "ind": "Pharmaceuticals", "rat": "Buy", "tgt": 1500, "pros": ["Respiratory dominance", "US footprint expanding"], "cons": ["Regulatory risks"]},
    {"t": "DIVISLAB", "n": "Divis Labs", "sec": "Pharma", "ind": "API", "rat": "Hold", "tgt": 4000, "pros": ["Cost leadership in API", "Custom synthesis growth"], "cons": ["Post-COVID revenue normalization"]},

    # Metals
    {"t": "TATASTEEL", "n": "Tata Steel", "sec": "Metals", "ind": "Steel", "rat": "Hold", "tgt": 170, "pros": ["India capacity expansion", "Captive iron ore"], "cons": ["Europe business drag", "Commodity cycle risk"]},
    {"t": "JSWSTEEL", "n": "JSW Steel", "sec": "Metals", "ind": "Steel", "rat": "Hold", "tgt": 950, "pros": ["Aggressive capacity additions", "Efficient converter"], "cons": ["High debt levels"]},
    {"t": "HINDALCO", "n": "Hindalco Industries", "sec": "Metals", "ind": "Aluminum", "rat": "Buy", "tgt": 700, "pros": ["Novelis drives steady cash", "EV aluminum demand"], "cons": ["LME price volatility"]},

    # Industrials & Infrastructure
    {"t": "LT", "n": "Larsen & Toubro", "sec": "Industrials", "ind": "Engineering", "rat": "Strong Buy", "tgt": 4200, "pros": ["Unmatched order book", "Infrastructure proxy"], "cons": ["Working capital intensive"]},
    {"t": "ADANIPORTS", "n": "Adani Ports", "sec": "Industrials", "ind": "Ports", "rat": "Buy", "tgt": 1500, "pros": ["Monopoly-like port assets", "Strong cash generation"], "cons": ["Group leverage concerns"]},
    {"t": "ULTRACEMCO", "n": "UltraTech Cement", "sec": "Industrials", "ind": "Cement", "rat": "Buy", "tgt": 11000, "pros": ["Unmatched scale", "Pricing power"], "cons": ["Energy cost volatility"]},
    {"t": "GRASIM", "n": "Grasim Industries", "sec": "Industrials", "ind": "Conglomerate", "rat": "Hold", "tgt": 2400, "pros": ["Holding company value", "Paints entry"], "cons": ["Holdco discount"]},

    # Telecom
    {"t": "BHARTIARTL", "n": "Bharti Airtel", "sec": "Telecom", "ind": "Telecommunications", "rat": "Buy", "tgt": 1500, "pros": ["Consistent ARPU growth", "Duopoly market structure"], "cons": ["High capex requirements"]}
]

class StockCache:
    def __init__(self):
        self.data = None
        self.timestamp = 0
        self.lock = Lock()
        self.ttl = 3600  # 1 hour
        self.is_warming = False

cache = StockCache()

def fetch_full_stock_data_internal():
    symbols = [s["t"] + ".NS" for s in STATIC_STOCKS]
    try:
        # Fetch 5y weekly history
        hist_df = yf.download(symbols, period="5y", interval="1wk", progress=False)
        tickers = yf.Tickers(" ".join(symbols))
        
        full_data = []
        for base_stock in STATIC_STOCKS:
            sym = base_stock["t"] + ".NS"
            info = tickers.tickers[sym].info
            
            def safe_get(key, default=None):
                val = info.get(key)
                if val is None or val == 'Infinity' or val == '-Infinity':
                    return default
                return val

            mc_raw = safe_get("marketCap", 0)
            mc_lcr = mc_raw / 1000000000000 if mc_raw else 0
            rev_raw = safe_get("totalRevenue", 0)
            rev_lcr = rev_raw / 1000000000000 if rev_raw else 0
            ni_raw = safe_get("netIncomeToCommon", 0)
            ni_lcr = ni_raw / 1000000000000 if ni_raw else 0

            try:
                if len(symbols) == 1:
                    close_series = hist_df['Close'].dropna().tolist()
                else:
                    close_series = hist_df['Close'][sym].dropna().tolist()
            except Exception:
                close_series = []

            stock_data = {
                **base_stock,
                "p": safe_get("currentPrice", safe_get("previousClose", 0)),
                "c1d": 0,
                "mc": round(mc_lcr, 2),
                "pe": round(safe_get("trailingPE", 0), 1) if safe_get("trailingPE") else None,
                "pb": round(safe_get("priceToBook", 0), 1) if safe_get("priceToBook") else None,
                "eps": round(safe_get("trailingEps", 0), 2) if safe_get("trailingEps") else None,
                "rev": round(rev_lcr, 2),
                "ni": round(ni_lcr, 2),
                "div": round(safe_get("dividendYield", 0), 2) if safe_get("dividendYield") else 0,
                "roe": round(safe_get("returnOnEquity", 0) * 100, 1) if safe_get("returnOnEquity") else None,
                "de": round(safe_get("debtToEquity", 0) / 100, 2) if safe_get("debtToEquity") else None,
                "beta": round(safe_get("beta", 0), 2) if safe_get("beta") else None,
                "gm": round(safe_get("grossMargins", 0) * 100, 1) if safe_get("grossMargins") else None,
                "nm": round(safe_get("profitMargins", 0) * 100, 1) if safe_get("profitMargins") else None,
                "om": round(safe_get("operatingMargins", 0) * 100, 1) if safe_get("operatingMargins") else None,
                "w52h": safe_get("fiftyTwoWeekHigh", 0),
                "w52l": safe_get("fiftyTwoWeekLow", 0),
                "vol": round(safe_get("averageVolume", 0) / 100000, 1) if safe_get("averageVolume") else 0,
                "hist": close_series
            }
            
            prev_close = safe_get("previousClose")
            current = stock_data["p"]
            if prev_close and current and prev_close > 0:
                stock_data["c1d"] = round(((current - prev_close) / prev_close) * 100, 2)
                
            full_data.append(stock_data)
        return full_data
    except Exception as e:
        print(f"Error in background fetch: {e}")
        return None

def background_warm_cache():
    print("Background thread: Warming up stock cache...")
    with cache.lock:
        cache.is_warming = True
    
    data = fetch_full_stock_data_internal()
    
    with cache.lock:
        if data:
            cache.data = data
            cache.timestamp = time.time()
            print("Background thread: Cache successfully warmed.")
        else:
            print("Background thread: Cache warmup failed.")
        cache.is_warming = False

# Start the background thread immediately upon module load
t = threading.Thread(target=background_warm_cache, daemon=True)
t.start()

def fetch_full_stock_data():
    with cache.lock:
        if cache.data and (time.time() - cache.timestamp) < cache.ttl:
            return cache.data
        if cache.is_warming:
            # If still warming, we must wait or return old data. 
            # If no old data, we fall through and do a synchronous fetch or wait.
            pass

    # If we get here, either cache expired and not warming, or warming is taking too long
    # We will block and fetch synchronously
    print("Fetching real market data synchronously...")
    data = fetch_full_stock_data_internal()
    if data:
        with cache.lock:
            cache.data = data
            cache.timestamp = time.time()
        return data
    else:
        return cache.data if cache.data else []
