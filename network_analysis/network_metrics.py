import numpy as np
import networkx as nx

def extract_network_metrics(G):
    """
    提取网络的拓扑特性指标
    
    参数:
    G (networkx.Graph): 网络图
    
    返回:
    dict: 包含各种网络指标的字典
    """
    metrics = {}
    
    # 如果网络为空或只有一个节点，返回NaN指标
    if G.number_of_nodes() <= 1 or G.number_of_edges() == 0:
        metrics['density'] = np.nan
        metrics['avg_degree_centrality'] = np.nan
        metrics['assortativity'] = np.nan
        return metrics
    
    # 检查图是否连通
    if not nx.is_connected(G):
        # 如果不连通，使用最大连通子图
        largest_cc = max(nx.connected_components(G), key=len)
        connected_G = G.subgraph(largest_cc).copy()
        print(f"警告: 图不连通，使用最大连通子图进行指标计算 ({len(largest_cc)}/{G.number_of_nodes()}个节点)")
    else:
        connected_G = G
    
    # 计算基本网络指标
    metrics['density'] = nx.density(G)
    
    # 计算每个节点的度中心性
    degree_centrality = nx.degree_centrality(G)
    metrics['avg_degree_centrality'] = np.mean(list(degree_centrality.values()))
    
    # 计算同配性 (度相关)
    try:
        metrics['assortativity'] = nx.degree_assortativity_coefficient(G, weight='weight')
    except:
        metrics['assortativity'] = np.nan
    
    return metrics

