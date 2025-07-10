import yfinance as yf

# Hardcoded duration and expense ratio values (source: ETF provider websites)
ETF_METADATA = {
    "SHY": {"duration": 1.9, "expense_ratio": 0.15},
    "IEI": {"duration": 4.5, "expense_ratio": 0.15},
    "IEF": {"duration": 7.6, "expense_ratio": 0.15},
    "TLT": {"duration": 17.5, "expense_ratio": 0.15},
    "AGG": {"duration": 6.4, "expense_ratio": 0.04},
    "LQD": {"duration": 9.0, "expense_ratio": 0.14},
    "HYG": {"duration": 3.7, "expense_ratio": 0.49}
}

def get_etf_data(tickers):
    etf_info = {}

    for symbol in tickers:
        try:
            print(f"📡 Fetching {symbol} data...")
            etf = yf.Ticker(symbol)
            data = etf.history(period="5d")
            info = etf.info

            price = data["Close"].iloc[-1]

            etf_info[symbol] = {
                "name": info.get("shortName", "Unknown ETF"),
                "price": price,
                "yield": info.get("yield", "N/A"),
                "duration": ETF_METADATA[symbol]["duration"],
                "expense_ratio": ETF_METADATA[symbol]["expense_ratio"]
            }

        except Exception as e:
            print(f"❌ Failed to fetch {symbol}: {e}")

    return etf_info
