import pandas as pd
from src.fmcg_basket.metrics import calculate_expected_commercial_value

def test_ecv_calculation():
    # Setup mock rules
    mock_rules = pd.DataFrame({
        'antecedents': ['Diapers'],
        'consequents': ['Beer'],
        'confidence': [0.5],
        'lift': [2.0]
    })

    mock_margins = {'Beer': 2.00}

    # Calculate ECV
    result = calculate_expected_commercial_value(mock_rules, mock_margins, basket_volume=1000)

    # ECV = Confidence (0.5) * Margin (2.00) * Volume (1000) = 1000.00
    expected_value = 1000.00

    assert 'Expected_Value_Per_1k_EUR' in result.columns
    assert result['Expected_Value_Per_1k_EUR'].iloc[0] == expected_value
    assert result['Consequent_Margin_EUR'].iloc[0] == 2.00
