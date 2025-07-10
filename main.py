
import pandas as pd
from liability_analysis import analyze_liabilities, load_liabilities_from_csv
from optimize_portfolio import run_optimization
from score import calculate_immunization_score
from visualize_cashflows import plot_cashflows

if __name__ == "__main__":
    # Load liability data
    liabilities = load_liabilities_from_csv("liabilities.csv")
    interest_rate = 0.05  # Example rate

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
    optimized_df = run_optimization(liability_pv, liability_duration, liability_convexity, liabilities)

    if optimized_df is None or optimized_df.empty:
        print("Optimization failed.")
        exit()

    # Save portfolio report
    optimized_df.to_csv("purchase_report.csv", index=False)
    print("Purchase report saved as purchase_report.csv")

    # Calculate and print immunization score
    score, breakdown = calculate_immunization_score(optimized_df, liability_pv, liability_duration, liability_convexity)
    print("\n--- Immunization Score ---")
    print(f"Score: {score:.2f}%")
    print(breakdown.to_string(index=False))

    # Save score breakdown to CSV
    breakdown.to_csv("immunization_score_report.csv", index=False)
    print("Score report saved as immunization_score_report.csv")

    # Plot asset vs liability cashflows (scatterplot)
    plot_cashflows(liabilities, optimized_df)
