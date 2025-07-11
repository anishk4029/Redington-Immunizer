
import pandas as pd
import numpy as np
from scipy.optimize import minimize

def run_optimization(pv_target, duration_target, convexity_target, liabilities):
    # Example bond data
    bonds = pd.DataFrame([
        {"symbol": "1Y_TBond", "price": 96.10, "duration": 1.0, "convexity": 1.05},
        {"symbol": "5Y_TBond", "price": 96.19, "duration": 4.8, "convexity": 24.0},
        {"symbol": "10Y_TBond", "price": 95.80, "duration": 8.8, "convexity": 90.0},
        {"symbol": "30Y_TBond", "price": 95.34, "duration": 18.5, "convexity": 280.0}
    ])

    prices = bonds["price"].values
    durations = bonds["duration"].values
    convexities = bonds["convexity"].values

    n = len(bonds)
    bounds = [(0, None) for _ in range(n)]

    def objective(weights):
        return abs(np.dot(weights, prices) - pv_target)

    def duration_constraint(weights):
        weighted_pv = np.dot(weights, prices)
        if weighted_pv == 0:
            return -1
        return np.dot(weights, prices * durations) / weighted_pv - duration_target

    def convexity_constraint(weights):
        weighted_pv = np.dot(weights, prices)
        if weighted_pv == 0:
            return -1
        return (np.dot(weights, prices * convexities) / weighted_pv) - convexity_target

    constraints = [
        {"type": "eq", "fun": lambda w: np.dot(w, prices) - pv_target},
        {"type": "eq", "fun": duration_constraint},
        {"type": "ineq", "fun": convexity_constraint}
    ]

    result = minimize(objective, x0=np.ones(n), bounds=bounds, constraints=constraints)

    if not result.success:
        print("--- Exact Optimization Failed ---")
        print("Trying approximate solution by relaxing all constraints...")
        constraints = [{"type": "eq", "fun": lambda w: np.dot(w, prices) - pv_target}]
        result = minimize(objective, x0=np.ones(n), bounds=bounds, constraints=constraints)

    weights = result.x if result.success else np.zeros(n)
    df = bonds.copy()
    df["Weight ($)"] = weights * prices
    df["Units to Buy"] = weights

    # Portfolio row
    total_value = np.dot(weights, prices)
    portfolio_duration = np.dot(weights, prices * durations) / total_value if total_value > 0 else 0
    portfolio_convexity = np.dot(weights, prices * convexities) / total_value if total_value > 0 else 0

    portfolio_row = {
        "symbol": "Portfolio",
        "price": total_value,
        "duration": portfolio_duration,
        "convexity": portfolio_convexity,
        "Weight ($)": total_value,
        "Units to Buy": np.nan
    }

    df.loc[len(df)] = portfolio_row

    # Construct asset cashflows (mocked as total cashflow at bond maturity)
    asset_cashflows = []
    for i, row in df.iterrows():
        if row["symbol"] == "Portfolio":
            continue
        if row["Units to Buy"] > 0.01:
            maturity = int(float(row["duration"]))
            total_cf = row["Units to Buy"] * 100
            asset_cashflows.append((maturity, total_cf))

    return df, asset_cashflows
