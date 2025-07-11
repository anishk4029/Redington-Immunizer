import pandas as pd
from liability_analysis import analyze_liabilities, load_liabilities_from_csv
from optimize_portfolio import run_optimization
from score import calculate_immunization_score
from visualize_cashflows import visualize_cashflows

if __name__ == "__main__":
    # Load liability data
    liabilities = load_liabilities_from_csv("liabilities.csv")
    interest_rate = 0.05  # Example interest rate

    if not liabilities:
        print("No liabilities loaded.")
        exit()

    # Analyze liabilities
    liability_pv, liability_duration, liability_convexity = analyze_liabilities(liabilities, interest_rate)
    print("\n--- Liability Analysis ---")
    print(f"Present Value: ${liability_pv:.2f}")
    print(f"Macaulay Duration: {liability_duration:.4f} years")
    print(f"Convexity: {liability_convexity:.4f}")

    # Run optimization
    optimized_df, asset_cashflows = run_optimization(
        liability_pv, liability_duration, liability_convexity, liabilities, interest_rate
    )

    if optimized_df is None or optimized_df.empty:
        print("Optimization failed.")
        exit()

    # Save portfolio report
    optimized_df.to_csv("purchase_report.csv", index=False)
    print("\nPurchase report saved as purchase_report.csv")

    # Calculate and print immunization score
    score_breakdown = calculate_immunization_score(
        liabilities, asset_cashflows, interest_rate, liability_convexity
    )
    print("\n--- Immunization Score ---")
    print(score_breakdown.to_string(index=False))

    # Save score report
    score_breakdown.to_csv("immunization_score_report.csv", index=False)
    print("Score report saved as immunization_score_report.csv")

    # Plot cashflows
    visualize_cashflows(liabilities, asset_cashflows)
    print("Cashflow plot saved as summed_cashflow_comparison.png")
