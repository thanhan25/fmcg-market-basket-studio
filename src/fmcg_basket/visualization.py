import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def plot_affinity_network(rules: pd.DataFrame, max_nodes: int = 30):
    """
    Generates a NetworkX graph showing product affinities based on Lift.
    """
    if rules.empty:
        return None

    fig, ax = plt.subplots(figsize=(12, 7))
    top_rules = rules.head(max_nodes)

    G = nx.from_pandas_edgelist(top_rules, 'antecedents', 'consequents', edge_attr='lift')
    pos = nx.spring_layout(G, k=0.6, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color='#003DA5', node_size=2500, alpha=0.9, edgecolors='white', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", font_color='white', ax=ax)

    weights = [edge[2]['lift'] for edge in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, width=weights, edge_color='#C4CED4', alpha=0.7, ax=ax)

    ax.axis('off')
    plt.tight_layout()
    return fig
