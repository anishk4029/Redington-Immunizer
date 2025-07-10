
import yfinance as yf
from fredapi import Fred
import pandas as pd

# --- CONFIG ---
FRED_API_KEY = "c4a5e36aea3b25bb7f5d8708b4f98a2e"  # Replace with your key
fred = Fred(api_key=FRED_API_KEY)

# --- ETFs to Track ---
ETF_TICKERS = ["TLT", "IEF", "SHY", "AGG", "LQD", "HYG", "BND"]

def get_etf_data(tickers):
    data = []
    for symbol in tickers:
        try:
            etf = yf.Ticker(symbol)
            info = etf.info

            data.append({
                "symbol": symbol,
                "price": info.get("regularMarketPrice"),
                "duration": info.get("duration", None),
                "convexity": info.get("convexity", None),
                "expenseRatio": info.get("annualReportExpenseRatio", None)
            })
        except Exception as e:
            print(f"Failed to fetch data for {symbol}: {e}")
    return data

def get_treasury_data():
    treasuries = [
        {"symbol": "1Y_TBond", "fred_id": "GS1", "duration": 1.0, "convexity": 1.05},
        {"symbol": "5Y_TBond", "fred_id": "GS5", "duration": 4.8, "convexity": 24.0},
        {"symbol": "10Y_TBond", "fred_id": "GS10", "duration": 8.8, "convexity": 90.0},
        {"symbol": "30Y_TBond", "fred_id": "GS30", "duration": 18.5, "convexity": 280.0},
    ]
    treasury_data = []
    for t in treasuries:
        try:
            rate = fred.get_series(t["fred_id"]).iloc[-1]
            price = 100 / (1 + rate / 100)  # Simplified bond pricing
            treasury_data.append({
                "symbol": t["symbol"],
                "price": round(price, 2),
                "duration": t["duration"],
                "convexity": t["convexity"],
                "expenseRatio": 0.0
            })
        except Exception as e:
            print(f"Failed to fetch {t['symbol']}: {e}")
    return treasury_data

def save_bond_data_to_csv(filename="bonds.csv"):
    etfs = get_etf_data(ETF_TICKERS)
    treasuries = get_treasury_data()
    all_data = etfs + treasuries
    df = pd.DataFrame(all_data)
    df.to_csv(filename, index=False)
    print(f"Saved bond data to {filename}")

if __name__ == "__main__":
    save_bond_data_to_csv()
