
# Commercial Strategy & Causal Impact

The FMCG Market Basket Studio transitions raw association rules from statistical artifacts to actionable margin-drivers.

## 1. Expected Commercial Value (ECV) vs. Lift

While traditional $Lift = \frac{P(A \cap B)}{P(A)P(B)}$ identifies affinity, it ignores gross margin. This engine calculates ECV by weighting the conditional probability of a consequent purchase by its unit margin, scaled over a standard 1,000-basket volume. This allows E-commerce category managers to prioritize a 1.2x Lift bundle yielding a €5.00 margin over a 3.0x Lift bundle yielding a €0.10 margin.

## 2. A/B Testing & Causal Inference Setup

Deploying these rules into a live recommendation system requires rigorous evaluation.

* **Methodology:** Randomized Control Trial (RCT) at the user-session level.
* **Treatment:** Real-time injection of top-3 ECV recommendations at checkout.
* **Control:** Baseline "Trending Products" recommendations.
* **Primary KPI:** Incremental Average Order Value (AOV).
* **Secondary KPI:** Recommendation Conversion Rate.

By establishing this framework, the Market Basket Studio serves not just as an analytical tool, but as the foundational layer for automated pricing simulators and long-term customer lifetime value (CLV) optimization.
