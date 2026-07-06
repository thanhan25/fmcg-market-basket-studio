from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List

app = FastAPI(
    title="FMCG Recommendation Engine",
    description="API serving ECV-ranked association rules for e-commerce cross-selling.",
    version="1.0.0"
)

try:
    rules_df = pd.read_csv("data/processed/association_rules.csv")
except FileNotFoundError:
    rules_df = pd.DataFrame()

class Recommendation(BaseModel):
    product: str
    confidence: float
    lift: float
    expected_value_eur: float

class RecommendationResponse(BaseModel):
    anchor: str
    recommendations: List[Recommendation]

@app.get("/health")
def health_check():
    return {"status": "operational", "rules_loaded": not rules_df.empty}

@app.get("/recommend/{product}", response_model=RecommendationResponse)
def get_recommendations(product: str, top_n: int = 3):
    if rules_df.empty:
        raise HTTPException(status_code=503, detail="Rules engine not initialized. Run the pipeline first.")

    recommendations = rules_df[rules_df['antecedents'].str.lower() == product.lower()]

    if recommendations.empty:
        return RecommendationResponse(anchor=product, recommendations=[])

    top_recs = recommendations.sort_values('Expected_Value_Per_1k_EUR', ascending=False).head(top_n)

    results = [
        Recommendation(
            product=row['consequents'],
            confidence=round(row['confidence'], 3),
            lift=round(row['lift'], 3),
            expected_value_eur=row['Expected_Value_Per_1k_EUR']
        )
        for _, row in top_recs.iterrows()
    ]

    return RecommendationResponse(anchor=product, recommendations=results)
