# 🛒 FMCG Market Basket Studio

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

An enterprise-grade Market Basket Analysis engine designed for FMCG Category Managers and E-commerce Recommendation Systems.
![Dashboard](assets/dashboard.png)

Unlike traditional data science repositories that stop at calculating "Lift", this studio calculates **Expected Commercial Value (ECV)**—allowing merchandisers to immediately identify the most profitable cross-selling bundles.

## Architecture

1. **Core Engine:** Polars/Pandas & MLxtend (Apriori Algorithm)
2. **BI Dashboard:** Streamlit UI for Category Managers (Network Graphs & ECV Tables)
3. **E-Commerce Integration:** FastAPI endpoint for real-time "Frequently Bought Together" recommendations.

## Quickstart

```bash
pip install -r requirements.txt
python src/fmcg_basket/engine.py
streamlit run app/dashboard.py
```
