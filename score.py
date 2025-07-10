import pandas as pd

def calculate_immunization_score(df, liability_pv, liability_duration, liability_convexity):
    portfolio_row = df[df["symbol"] == "Portfolio"]
    if portfolio_row.empty:
        return 0.0, pd.DataFrame(columns=["Metric", "Target", "Portfolio", "Deviation", "Score %"])

    port_pv = portfolio_row["price"].values[0]
    port_duration = portfolio_row["duration"].values[0]
    port_convexity = portfolio_row["convexity"].values[0]

    # Calculate price deviation
    price_diff = abs(port_pv - liability_pv) / liability_pv
    price_score = max(0.0, 34.0 * (1 - price_diff * 100))

    # Duration score (penalize under/overshoot)
    duration_diff = abs(port_duration - liability_duration) / liability_duration
    duration_score = max(0.0, 33.0 * (1 - duration_diff * 100))

    # Convexity score (only penalize if convexity is below liability's)
    if port_convexity >= liability_convexity:
        convexity_score = 33.0
        convexity_deviation = 0
    else:
        convexity_deviation = (liability_convexity - port_convexity) / liability_convexity
        convexity_score = max(0.0, 33.0 * (1 - convexity_deviation * 100))

    total_score = price_score + duration_score + convexity_score

    breakdown = pd.DataFrame([
        ["Present Value", liability_pv, port_pv, f"{price_diff * 100:.2f}%", f"{price_score:.2f}%"],
        ["Duration", liability_duration, port_duration, f"{duration_diff * 100:.2f}%", f"{duration_score:.2f}%"],
        ["Convexity", liability_convexity, port_convexity, f"{convexity_deviation * 100:.2f}%", f"{convexity_score:.2f}%"]
    ], columns=["Metric", "Target", "Portfolio", "Deviation", "Score %"])

    return total_score, breakdown
