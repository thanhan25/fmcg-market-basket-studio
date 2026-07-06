import streamlit as st
import pandas as pd
from src.fmcg_basket.visualization import plot_affinity_network

st.set_page_config(page_title="FMCG Market Basket Studio", layout="wide", page_icon="🛒")

st.title("🛒 FMCG Market Basket Studio")
st.markdown("Optimize cross-selling bundles using FP-Growth and Expected Commercial Value (ECV).")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/processed/association_rules.csv")
    except FileNotFoundError:
        st.error("Dataset missing. Execute pipeline: `uv run python -m src.fmcg_basket.engine`")
        return pd.DataFrame()

rules = load_data()

if not rules.empty:
    st.sidebar.header("🎯 Preset Scenarios")
    preset = st.sidebar.radio("Select a business view:", ["Custom Filter", "Diapers Cross-Sell", "High-Margin Wine"])

    # Preset Logic
    default_anchor = "All"
    default_lift = 1.2
    if preset == "Diapers Cross-Sell":
        default_anchor = "Diapers"
        default_lift = 1.5
    elif preset == "High-Margin Wine":
        default_anchor = "Wine"
        default_lift = 1.1

    st.sidebar.header("🎛️ Rule Filters")
    min_lift = st.sidebar.slider("Minimum Lift Threshold", 1.0, 5.0, default_lift)

    products = ["All"] + sorted(rules['antecedents'].unique().tolist())
    anchor_idx = products.index(default_anchor) if default_anchor in products else 0
    product = st.sidebar.selectbox("Anchor Product (Antecedent)", products, index=anchor_idx)

    filtered_rules = rules[rules['lift'] >= min_lift]
    if product != "All":
        filtered_rules = filtered_rules[filtered_rules['antecedents'] == product]

    tab1, tab2 = st.tabs(["📊 Commercial Strategy", "🕸️ Network Affinity"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Rules", len(filtered_rules))

        col2.metric(
            "Max ECV (per 1k baskets)",
            f"€{filtered_rules['Expected_Value_Per_1k_EUR'].max():.2f}" if not filtered_rules.empty else "€0",
            help="Expected Commercial Value: Confidence * Consequent Margin * 1,000"
        )
        col3.metric(
            "Highest Lift Bundle",
            f"{filtered_rules['lift'].max():.2f}x" if not filtered_rules.empty else "0x",
            help="How many times more likely the items are bought together compared to random chance."
        )

        st.subheader("Ranked Cross-Sell Opportunities")
        display_cols = ['antecedents', 'consequents', 'confidence', 'lift', 'Expected_Value_Per_1k_EUR']
        st.dataframe(
            filtered_rules[display_cols].sort_values('Expected_Value_Per_1k_EUR', ascending=False),
            use_container_width=True
        )

        # API Sync Example
        if product != "All":
            st.markdown("---")
            st.subheader("💻 API Integration Equivalent")
            st.code(
                f"curl -X GET 'http://localhost:8000/recommend/{product.lower()}?min_lift={min_lift}'",
                language="bash",
                )

    with tab2:
        st.subheader("Product Affinity Graph")
        if not filtered_rules.empty:
            fig = plot_affinity_network(filtered_rules)
            if fig:
                st.pyplot(fig)
        else:
            st.info("No rules match the current filter criteria.")
