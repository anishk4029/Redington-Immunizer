
import pandas as pd
import matplotlib.pyplot as plt

def plot_cashflows(liabilities, optimized_df):
    # Compute asset cash flows based on optimized portfolio
    asset_cashflows = []
    for _, row in optimized_df.iterrows():
        if row["symbol"] != "Portfolio" and row["Units to Buy"] > 0.01:
            years = 30  # assume 30-year maturity
            par = 100
            coupon = 3  # fixed $3 annual coupon per bond
            units = row["Units to Buy"]

            for t in range(1, years):
                asset_cashflows.append((t, coupon * units))
            asset_cashflows.append((years, (coupon + par) * units))  # final year

    asset_df = pd.DataFrame(asset_cashflows, columns=["time", "amount"])
    liabilities_df = pd.DataFrame(liabilities, columns=["time", "amount"])

    # Generate scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(liabilities_df["time"], liabilities_df["amount"], color='red', label="Liabilities", marker='o')
    plt.scatter(asset_df["time"], asset_df["amount"], color='green', label="Assets", marker='x')

    plt.xlabel("Time (Years)")
    plt.ylabel("Cash Flow ($)")
    plt.title("Asset vs Liability Cash Flows (Scatter Plot)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cashflow_comparison_scatter.png")
    plt.show()
