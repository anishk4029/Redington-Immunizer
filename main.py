
import pandas as pd
from liability_analysis import analyze_liabilities, load_liabilities_from_csv
from optimize_portfolio import run_optimization
from score import calculate_immunization_score
from visualize_cashflows import visualize_cashflows

if __name__ == "__main__":
    liabilities = load_liabilities_from_csv("liabilities.csv")
    interest_rate = 0.05

    if not liabilities:
        print("No liabilities loaded.")
        exit()

    liability_pv, liability_duration, liability_convexity = analyze_liabilities(liabilities, interest_rate)
    print("\n--- Liability Analysis ---")
    print(f"Present Value: ${liability_pv:.2f}")
    print(f"Macaulay Duration: {liability_duration:.4f} years")
    print(f"Convexity: {liability_convexity:.4f}")

    optimized_df, asset_cashflows = run_optimization(liability_pv, liability_duration, liability_convexity, liabilities)

    if optimized_df is None or optimized_df.empty:
        print("Optimization failed.")
        exit()

    optimized_df.to_csv("purchase_report.csv", index=False)
    print("Purchase report saved as purchase_report.csv")

    score, breakdown = calculate_immunization_score(optimized_df, liability_pv, liability_duration, liability_convexity)
    print("\n--- Immunization Score ---")
    print(f"Score: {score:.2f}%")
    print(breakdown.to_string(index=False))

    breakdown.to_csv("immunization_score_report.csv", index=False)
    print("Score report saved as immunization_score_report.csv")

    # New visualization
    visualize_cashflows(liabilities, asset_cashflows)
