import pandas as pd

def calculate_expected_commercial_value(rules: pd.DataFrame, margins: dict, volume: int = 1000) -> pd.DataFrame:
    """
    Calculates Expected Commercial Value (ECV) for association rules.
    ECV = Confidence * Margin of Consequent * Baseline Volume
    """
    # Map margins; default to 1.0 if not found in dictionary to prevent NaN
    consequent_margins = rules["consequents"].map(margins).fillna(1.0)

    rules["Expected_Value_Per_1k_EUR"] = (
        rules["confidence"] * consequent_margins * (volume / 1000)
    )
    return rules
