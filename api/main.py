from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI(title="FMCG Recommendation API")

try:
    rules_df = pd.read_csv("data/processed/association_rules.csv")
except FileNotFoundError:
    rules_df = pd.DataFrame()

@app.get("/")
def health_check():
    return {"status": "active", "engine": "FMCG Market Basket Studio"}

@app.get("/recommend/{product}")
def get_recommendations(product: str, top_n: int = 3):
    if rules_df.empty:
        raise HTTPException(status_code=500, detail="Rules engine not initialized.")
        
    # Filter for the anchor product
    recommendations = rules_df[rules_df['antecedents'].str.lower() == product.lower()]
    
    if recommendations.empty:
        return {"anchor": product, "recommendations": []}
        
    # Sort by Expected Commercial Value
    top_recs = recommendations.sort_values('Expected_Value_Per_1k_EUR', ascending=False).head(top_n)
    
    results = []
    for _, row in top_recs.iterrows():
        results.append({
            "product": row['consequents'],
            "confidence": round(row['confidence'], 2),
            "lift": round(row['lift'], 2),
            "expected_value_eur": row['Expected_Value_Per_1k_EUR']
        })
        
    return {"anchor": product, "recommendations": results}