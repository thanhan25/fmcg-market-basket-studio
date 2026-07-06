import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import fpgrowth, association_rules
import os
from src.fmcg_basket.metrics import calculate_expected_commercial_value

def generate_synthetic_data(num_transactions: int = 10000):
    """Generates synthetic FMCG transactions for demonstration."""
    print(f"Generating {num_transactions} synthetic FMCG transactions...")
    products = ['Diapers', 'Baby Wipes', 'Beer', 'Chips', 'Milk', 'Bread', 'Butter', 'Eggs', 'Wine', 'Cheese']
    margins = {'Diapers': 4.50, 'Baby Wipes': 1.20, 'Beer': 2.00, 'Chips': 0.80,
               'Milk': 0.50, 'Bread': 0.60, 'Butter': 0.70, 'Eggs': 0.90, 'Wine': 5.00, 'Cheese': 2.50}

    transactions = []
    for _ in range(num_transactions):
        basket = []
        rand_val = np.random.rand()
        if rand_val > 0.7:
            basket.extend(['Diapers', 'Baby Wipes'])
            if np.random.rand() > 0.4:
                basket.append('Beer')
        elif rand_val > 0.4:
            basket.extend(['Milk', 'Bread', 'Butter'])
            if np.random.rand() > 0.5:
                basket.append('Eggs')
        else:
            basket.extend(['Wine', 'Cheese'])
            if np.random.rand() > 0.6:
                basket.append('Bread')

        for p in products:
            if np.random.rand() > 0.92 and p not in basket:
                basket.append(p)
        transactions.append(basket)

    df = pd.DataFrame(transactions)
    df_encoded = pd.get_dummies(df.unstack().dropna()).groupby(level=1).sum()
    df_encoded = df_encoded.map(lambda x: True if x > 0 else False)

    os.makedirs('data/processed', exist_ok=True)
    pd.DataFrame(list(margins.items()), columns=['Product', 'Margin']).to_csv('data/processed/margins.csv', index=False)
    return df_encoded, margins

def mine_rules_fpgrowth(df: pd.DataFrame, margins: dict, min_support: float = 0.02, min_lift: float = 1.2):
    """Mines association rules using the optimized FP-Growth algorithm."""
    print("Mining association rules via FP-Growth...")
    frequent_itemsets = fpgrowth(df, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)

    rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x)[0])
    rules['consequents'] = rules['consequents'].apply(lambda x: list(x)[0])

    rules = calculate_expected_commercial_value(rules, margins)

    os.makedirs('data/processed', exist_ok=True)
    rules.to_csv('data/processed/association_rules.csv', index=False)
    print("Optimization complete. Rules saved to data/processed/association_rules.csv")
    return rules

if __name__ == "__main__":
    df_encoded, margins = generate_synthetic_data()
    rules = mine_rules_fpgrowth(df_encoded, margins)
