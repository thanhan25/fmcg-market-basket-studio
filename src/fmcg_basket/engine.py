import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
import os

def generate_synthetic_data(num_transactions=5000):
    """Generates realistic FMCG transaction data."""
    print("Generating synthetic FMCG transactions...")
    products = ['Diapers', 'Baby Wipes', 'Beer', 'Chips', 'Milk', 'Bread', 'Butter', 'Eggs', 'Wine', 'Cheese']
    
    # Fake margins (in EUR) for Expected Commercial Value (ECV) calculation
    margins = {'Diapers': 4.50, 'Baby Wipes': 1.20, 'Beer': 2.00, 'Chips': 0.80, 
               'Milk': 0.50, 'Bread': 0.60, 'Butter': 0.70, 'Eggs': 0.90, 'Wine': 5.00, 'Cheese': 2.50}
    
    transactions = []
    for _ in range(num_transactions):
        basket = []
        # Pattern 1: Parents
        if np.random.rand() > 0.7:
            basket.extend(['Diapers', 'Baby Wipes'])
            if np.random.rand() > 0.5: basket.append('Beer') # The classic retail myth
        # Pattern 2: Breakfast
        elif np.random.rand() > 0.6:
            basket.extend(['Milk', 'Bread', 'Butter'])
            if np.random.rand() > 0.5: basket.append('Eggs')
        # Pattern 3: Evening
        else:
            basket.extend(['Wine', 'Cheese'])
            if np.random.rand() > 0.7: basket.append('Bread')
            
        # Add random noise
        for p in products:
            if np.random.rand() > 0.90 and p not in basket:
                basket.append(p)
                
        transactions.append(basket)
        
    # One-hot encode
    df = pd.DataFrame(transactions)
    df_encoded = pd.get_dummies(df.unstack().dropna()).groupby(level=1).sum()
    
    # Cast to boolean to satisfy mlxtend performance requirements
    df_encoded = df_encoded.map(lambda x: True if x > 0 else False)
    
    # Save margins for ECV
    pd.DataFrame(list(margins.items()), columns=['Product', 'Margin']).to_csv('data/processed/margins.csv', index=False)
    return df_encoded, margins

def mine_rules(df, margins):
    """Runs Apriori and calculates Expected Commercial Value (ECV)."""
    print("Mining association rules...")
    frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
    
    # Clean up frozensets for easier reading
    rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x)[0])
    rules['consequents'] = rules['consequents'].apply(lambda x: list(x)[0])
    
    # Calculate Expected Commercial Value (ECV) per 1000 baskets
    # ECV = Confidence (probability they buy) * Margin of the consequent product * 1000
    margin_map = pd.DataFrame(list(margins.items()), columns=['Product', 'Margin']).set_index('Product')['Margin'].to_dict()
    rules['Consequent_Margin_EUR'] = rules['consequents'].map(margin_map)
    rules['Expected_Value_Per_1k_EUR'] = (rules['confidence'] * rules['Consequent_Margin_EUR'] * 1000).round(2)
    
    # Sort by Commercial Value
    rules = rules.sort_values('Expected_Value_Per_1k_EUR', ascending=False)
    
    os.makedirs('data/processed', exist_ok=True)
    rules.to_csv('data/processed/association_rules.csv', index=False)
    print("Rules saved to data/processed/association_rules.csv")
    return rules

if __name__ == "__main__":
    df_encoded, margins = generate_synthetic_data()
    rules = mine_rules(df_encoded, margins)
    print(rules[['antecedents', 'consequents', 'lift', 'Expected_Value_Per_1k_EUR']].head())