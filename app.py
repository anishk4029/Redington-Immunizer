import streamlit as st
import pandas as pd
from liability_analysis import analyze_liabilities
from optimize_portfolio import run_optimization
from score import calculate_immunization_score
from visualize_cashflows import visualize_cashflows

st.set_page_config(page_title="Redington Immunizer", layout="wide")
st.title("🔐 Redington Immunizer")

# Upload CSV
uploaded_file = st.file_uploader("Upload your liability CSV file", type="csv")

if uploaded_file:
    liabilities_df = pd.read_csv(uploaded_file)
    liabilities = list(zip(liabilities_df["time"], liabilities_df["amount"]))

    # Set interest rate
    interest_rate = st.number_input("Enter Interest Rate (as decimal)", min_value=0.0, max_value=1.0, value=0.05)

    # Analyze liabilities
    pv, duration, convexity = analyze_liabilities(liabilities, interest_rate)

    st.subheader("📊 Liability Analysis")
    st.write(f"**Present Value:** ${pv:,.2f}")
    st.write(f"**Macaulay Duration:** {duration:.4f} years")
    st.write(f"**Convexity:** {convexity:.4f}")

    # Run optimization
    optimized_df = run_optimization(pv, duration, convexity, liabilities)

    if optimized_df is not None and not optimized_df.empty:
        st.subheader("💼 Optimized Portfolio")
        st.dataframe(optimized_df)

        # Show score
        score, breakdown = calculate_immunization_score(optimized_df, pv, duration, convexity)
        st.subheader("📈 Immunization Score")
        st.write(f"**Score:** {score:.2f}%")
        st.dataframe(breakdown)

        # Generate and show plot
        st.subheader("📍 Cashflow Comparison (Scatter Plot)")
        visualize_cashflows(liabilities, optimized_df)
        st.image("cashflow_comparison_scatter.png")
    else:
        st.error("Optimization failed. Please try different inputs.")
