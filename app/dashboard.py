import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="FMCG Market Basket Studio", layout="wide")
st.title("🛒 FMCG Market Basket Studio")
st.markdown("Discover actionable cross-sell bundles and expected commercial value (ECV).")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/processed/association_rules.csv")
    except FileNotFoundError:
        st.error("Data not found. Please run `python src/fmcg_basket/engine.py` first.")
        return pd.DataFrame()

rules = load_data()

if not rules.empty:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Filter Rules")
        min_lift = st.slider("Minimum Lift", 1.0, 5.0, 1.5)
        product = st.selectbox("Anchor Product (Antecedent)", ["All"] + list(rules['antecedents'].unique()))
        
        filtered_rules = rules[rules['lift'] >= min_lift]
        if product != "All":
            filtered_rules = filtered_rules[filtered_rules['antecedents'] == product]
            
        st.metric("Total Rules Found", len(filtered_rules))
        
    with col2:
        st.subheader("Top Cross-Sell Opportunities (Ranked by ECV)")
        display_cols = ['antecedents', 'consequents', 'support', 'confidence', 'lift', 'Expected_Value_Per_1k_EUR']
        st.dataframe(filtered_rules[display_cols].head(10), use_container_width=True)

    st.markdown("---")
    st.subheader("Product Affinity Network Graph")
    
    # Draw Network
    fig, ax = plt.subplots(figsize=(10, 6))
    G = nx.from_pandas_edgelist(filtered_rules.head(20), 'antecedents', 'consequents', edge_attr='lift')
    pos = nx.spring_layout(G, k=0.5)
    
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=2000, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    
    edges = G.edges(data=True)
    weights = [edge[2]['lift'] for edge in edges]
    nx.draw_networkx_edges(G, pos, width=weights, edge_color='gray', alpha=0.5)
    
    plt.axis('off')
    st.pyplot(fig)