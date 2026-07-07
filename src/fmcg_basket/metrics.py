import pandas as pd

def calculate_expected_commercial_value(rules: pd.DataFrame, margins: dict, volume: int = 1000) -> pd.DataFrame:
    """
    Calculates Expected Commercial Value (ECV) for association rules.
    ECV = Confidence * Margin of Consequent * Baseline Volume
    """
    # 1. Map margins to a new column so the API and Dashboard can reference it if needed
    rules["Consequent_Margin_EUR"] = rules["consequents"].map(margins).fillna(1.0)

    # 2. Calculate the final ECV metric
    rules["Expected_Value_Per_1k_EUR"] = (
        rules["confidence"] * rules["Consequent_Margin_EUR"] * volume
    )
    return rules
