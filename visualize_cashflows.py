
import pandas as pd
import matplotlib.pyplot as plt

def visualize_cashflows(liabilities, asset_cashflows):
    # Convert to DataFrames
    liabilities_df = pd.DataFrame(liabilities, columns=["time", "amount"])
    assets_df = pd.DataFrame(asset_cashflows, columns=["time", "amount"])

    # Aggregate amounts by time
    liability_sums = liabilities_df.groupby("time")["amount"].sum().reset_index()
    asset_sums = assets_df.groupby("time")["amount"].sum().reset_index()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(liability_sums["time"], liability_sums["amount"], marker='o', label='Liabilities', linewidth=2)
    plt.plot(asset_sums["time"], asset_sums["amount"], marker='s', label='Assets', linewidth=2)

    plt.xlabel("Time (Years)")
    plt.ylabel("Cashflow Amount ($)")
    plt.title("Summed Asset vs Liability Cashflows Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("summed_cashflow_comparison.png")
    plt.show()
