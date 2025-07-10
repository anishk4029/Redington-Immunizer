
import pandas as pd

def analyze_liabilities(liabilities, interest_rate):
    v = 1 / (1 + interest_rate)
    pv = sum(cf * v**t for t, cf in liabilities)
    duration = sum(t * cf * v**t for t, cf in liabilities) / pv
    convexity = sum(t * (t + 1) * cf * v**t for t, cf in liabilities) / (pv * (1 + interest_rate)**2)
    return pv, duration, convexity

def load_liabilities_from_csv(filepath):
    try:
        df = pd.read_csv(filepath, skipinitialspace=True)
        print("CSV Loaded:\n", df.head())
        liabilities = list(zip(df['time'], df['amount']))
        return liabilities
    except Exception as e:
        print("Error reading CSV:", e)
        return []
