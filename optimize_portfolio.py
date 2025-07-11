import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Sample fixed bond universe (can be replaced with live data)
BOND_DATA = [
    {"symbol": "1Y_TBond", "price": 96.10, "duration": 1.0, "convexity": 1.05},
    {"symbol": "5Y_TBond", "price": 96.19, "duration": 4.8, "convexity": 24.0},
    {"symbol": "10Y_TBond", "price": 95.80, "duration": 8.8, "convexity": 90.0},
    {"symbol": "30Y_TBond", "price": 95.34, "duration": 18.5, "convexity": 280.0},
]

def run_optimization(pv_target, duration_target, convexity_target, liabilities, interest_rate):
    bonds = pd.DataFrame(BOND_DATA)
    prices = bonds["price"].values
    durations = bonds["duration"].values
    convexities = bonds["convexity"].values

    n = len(bonds)

    # Objective: minimize total price (equivalent to matching PV)
    def objective(weights):
        return np.dot(weights, prices)

    # Constraints for Redington immunization
    constraints = [
        {"type": "eq", "fun": lambda w: np.dot(w, prices) - pv_target},
        {"type": "eq", "fun": lambda w: np.dot(w, prices * durations) - pv_target * duration_target},
        {"type": "ineq", "fun": lambda w: np.dot(w, prices * convexities) - pv_target * convexity_target},
    ]

    bounds = [(0, None) for _ in range(n)]
    initial = np.ones(n)

    result = minimize(objective, initial, bounds=bounds, constraints=constraints)

    if not result.success:
        print("--- Exact Optimization Failed ---")
        print("Trying approximate solution by relaxing all constraints...")
        relaxed_constraints = [
            {"type": "eq", "fun": lambda w: np.dot(w, prices) - pv_target},
        ]
        result = minimize(objective, initial, bounds=bounds, constraints=relaxed_constraints)
        if not result.success:
            print("Approximate optimization also failed.")
            return None, []

    weights = result.x
    bonds["Weight ($)"] = weights * prices
    bonds["Units to Buy"] = weights

    # Filter out near-zero weight assets for clean reporting
    bonds = bonds[bonds["Units to Buy"] > 0.01].copy()

    # Add portfolio summary
    total_value = bonds["Weight ($)"].sum()
    portfolio_duration = np.dot(weights, prices * durations) / total_value
    portfolio_convexity = np.dot(weights, prices * convexities) / total_value
    portfolio_row = pd.DataFrame.from_dict({
        "symbol": ["Portfolio"],
        "price": [pv_target],
        "duration": [portfolio_duration],
        "convexity": [portfolio_convexity],
        "Weight ($)": [total_value],
        "Units to Buy": [np.nan]
    })
    df = pd.concat([bonds, portfolio_row], ignore_index=True)

    # Generate asset cashflows for visualization
    asset_cashflows = []
    for i, row in bonds.iterrows():
        term = int(round(row["duration"]))
        unit = row["Units to Buy"]
        for t in range(1, term + 1):
            asset_cashflows.append((t, unit * 100))
        asset_cashflows.append((term, unit * 100))  # par value return

    return df, asset_cashflows
