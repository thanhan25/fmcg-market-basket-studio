from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
from typing import List

app = FastAPI(
    title="FMCG Recommendation Engine",
    description="API serving ECV-ranked association rules for e-commerce cross-selling.",
    version="1.0.0"
)

# Load engine data globally
try:
    rules_df = pd.read_csv("data/processed/association_rules.csv")
    # Normalize products for robust querying
    rules_df['antecedents'] = rules_df['antecedents'].str.strip().str.lower()
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
def get_recommendations(
    product: str,
    top_n: int = Query(3, ge=1, le=10),
    min_lift: float = Query(1.0, ge=1.0),
    min_confidence: float = Query(0.1, ge=0.0)
):
    """Fetch 'Frequently Bought Together' items for a given anchor product."""
    if rules_df.empty:
        raise HTTPException(status_code=503, detail="Rules engine not initialized. Run pipeline first.")

    # Normalize query to lowercase for matching
    product_query = product.strip().lower()

    # Ensure dataframe antecedents are lowercase for the comparison, but keep original for response
    mask = rules_df['antecedents'].str.lower() == product_query
    recommendations = rules_df[
        mask &
        (rules_df['lift'] >= min_lift) &
        (rules_df['confidence'] >= min_confidence)
    ]

    if recommendations.empty:
        return RecommendationResponse(anchor=product.title(), recommendations=[])

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

    return RecommendationResponse(anchor=product.title(), recommendations=results)
