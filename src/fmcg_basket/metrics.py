import pandas as pd

def calculate_expected_commercial_value(rules: pd.DataFrame, margins: dict, basket_volume: int = 1000) -> pd.DataFrame:
    """
    Calculates the Expected Commercial Value (ECV) of a cross-sell rule.
    ECV = Confidence * Consequent Margin * Expected Basket Volume
    """
    if rules.empty:
        return rules

    margin_df = pd.DataFrame(list(margins.items()), columns=['Product', 'Margin']).set_index('Product')
    margin_map = margin_df['Margin'].to_dict()

    rules = rules.copy()
    rules['Consequent_Margin_EUR'] = rules['consequents'].map(margin_map)
    rules['Expected_Value_Per_1k_EUR'] = (rules['confidence'] * rules['Consequent_Margin_EUR'] * basket_volume).round(2)

    return rules.sort_values('Expected_Value_Per_1k_EUR', ascending=False)
