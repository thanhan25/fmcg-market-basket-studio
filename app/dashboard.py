import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="FMCG Market Basket Studio", layout="wide", page_icon="🛒")

st.title("🛒 FMCG Market Basket Studio")
st.markdown("Optimize cross-selling bundles using FP-Growth and Expected Commercial Value (ECV).")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/processed/association_rules.csv")
    except FileNotFoundError:
        st.error("Dataset missing. Execute pipeline: `uv run python src/fmcg_basket/engine.py`")
        return pd.DataFrame()

rules = load_data()

if not rules.empty:
    st.sidebar.header("Rule Filters")
    min_lift = st.sidebar.slider("Minimum Lift Threshold", 1.0, 5.0, 1.2)
    product = st.sidebar.selectbox("Anchor Product (Antecedent)", ["All"] + list(rules['antecedents'].unique()))

    filtered_rules = rules[rules['lift'] >= min_lift]
    if product != "All":
        filtered_rules = filtered_rules[filtered_rules['antecedents'] == product]

    tab1, tab2 = st.tabs(["📊 Commercial Strategy", "🕸️ Network Affinity"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Rules", len(filtered_rules))
        col2.metric(
            "Max ECV (per 1k baskets)",
            f"€{filtered_rules['Expected_Value_Per_1k_EUR'].max():.2f}" if not filtered_rules.empty else "€0")
        col3.metric("Highest Lift Bundle", f"{filtered_rules['lift'].max():.2f}x" if not filtered_rules.empty else "0x")

        st.subheader("Ranked Cross-Sell Opportunities")
        display_cols = ['antecedents', 'consequents', 'confidence', 'lift', 'Expected_Value_Per_1k_EUR']
        st.dataframe(filtered_rules[display_cols].sort_values(
            'Expected_Value_Per_1k_EUR',
            ascending=False),
            use_container_width=True,
            )

    with tab2:
        st.subheader("Product Affinity Graph")
        if not filtered_rules.empty:
            fig, ax = plt.subplots(figsize=(12, 7))
            G = nx.from_pandas_edgelist(filtered_rules.head(30), 'antecedents', 'consequents', edge_attr='lift')
            pos = nx.spring_layout(G, k=0.6, seed=42)

            # Draw nodes and edges
            nx.draw_networkx_nodes(G, pos, node_color='#003DA5', node_size=2500, alpha=0.9, edgecolors='white')
            nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", font_color='white')
            weights = [edge[2]['lift'] for edge in G.edges(data=True)]
            nx.draw_networkx_edges(G, pos, width=weights, edge_color='#C4CED4', alpha=0.7)

            plt.axis('off')
            st.pyplot(fig)
        else:
            st.info("No rules match the current filter criteria.")
