
import pandas as pd
import numpy as np
from scipy.optimize import minimize

def run_optimization(target_pv, target_duration, target_convexity, liabilities):
    print(f"PV Target: {target_pv}")
    print(f"Duration Target Range: {target_pv * target_duration * 0.85} to {target_pv * target_duration * 1.15}")
    print(f"Min Convexity Target: {target_pv * target_convexity * 1.25}")

    # Example bond data (could be replaced with live data)
    data = [
        {"symbol": "1Y_TBond", "price": 96.10, "duration": 1.0, "convexity": 1.05},
        {"symbol": "5Y_TBond", "price": 96.19, "duration": 4.8, "convexity": 24.0},
        {"symbol": "10Y_TBond", "price": 95.80, "duration": 8.8, "convexity": 90.0},
        {"symbol": "30Y_TBond", "price": 95.34, "duration": 18.5, "convexity": 280.0}
    ]
    df = pd.DataFrame(data)

    prices = df["price"].values
    durations = df["duration"].values
    convexities = df["convexity"].values
    n = len(df)

    def objective(weights):
        return np.sum(weights)  # Minimize total investment

    def pv_constraint(weights):
        return np.dot(weights, prices) - target_pv

    def duration_constraint(weights):
        return np.dot(weights, prices * durations) - target_pv * target_duration

    def convexity_constraint(weights):
        return np.dot(weights, prices * convexities) - target_pv * target_convexity

    bounds = [(0, None)] * n
    constraints = [
        {"type": "eq", "fun": pv_constraint},
        {"type": "eq", "fun": duration_constraint},
        {"type": "ineq", "fun": convexity_constraint}
    ]

    result = minimize(objective, x0=np.ones(n), bounds=bounds, constraints=constraints)

    if not result.success:
        print("--- Exact Optimization Failed ---")
        print("Trying approximate solution by relaxing all constraints...")

        constraints = [
            {"type": "eq", "fun": pv_constraint},
            {"type": "ineq", "fun": convexity_constraint}
        ]

        result = minimize(objective, x0=np.ones(n), bounds=bounds, constraints=constraints)

        if not result.success:
            print("Approximate optimization also failed.")
            return None

        print("--- Approximate Match Found ---")
    else:
        print("--- Exact Match Found ---")

    df["Weight ($)"] = result.x * prices
    df["Units to Buy"] = result.x

    # Filter out assets with negligible units
    filtered = df[df["Units to Buy"] > 0.01].copy()

    total_value = (filtered["price"] * filtered["Units to Buy"]).sum()
    weighted_duration = (filtered["duration"] * filtered["price"] * filtered["Units to Buy"]).sum() / total_value
    weighted_convexity = (filtered["convexity"] * filtered["price"] * filtered["Units to Buy"]).sum() / total_value

    portfolio_row = {
        "symbol": "Portfolio",
        "price": total_value,
        "duration": weighted_duration,
        "convexity": weighted_convexity,
        "Weight ($)": total_value,
        "Units to Buy": None
    }

    df = pd.concat([df, pd.DataFrame([portfolio_row])], ignore_index=True)
    return df
