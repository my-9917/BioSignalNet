import numpy as np
import networkx as nx

def construct_similarity_graph(signals, similarity_measure='correlation', threshold=0.0):
    """
    基于信号间的相似度构建网络图
    
    参数:
    signals (np.array): 形状为 [n_channels, n_timepoints] 的信号数据
    similarity_measure (str): 相似度度量方式，可选 'correlation', 'mutual_info', 'phase_sync'
    threshold (float): 相似度阈值，低于此值的边将被过滤
    
    返回:
    networkx.Graph: 构建的网络图
    """
    n_channels = signals.shape[0]
    G = nx.Graph()
    
    # 添加节点
    for i in range(n_channels):
        G.add_node(i)
    
    # 计算相似度并添加边
    for i in range(n_channels):
        for j in range(i+1, n_channels):
            if similarity_measure == 'correlation':
                # 使用相关系数作为相似度指标
                corr = np.abs(np.corrcoef(signals[i], signals[j])[0, 1])
                if not np.isnan(corr) and corr > threshold:
                    G.add_edge(i, j, weight=corr)
            # 可以添加其他相似度度量方式
            # elif similarity_measure == 'mutual_info':
            #     # 使用互信息作为相似度指标
            #     mi = compute_mutual_info(signals[i], signals[j])
            #     if not np.isnan(mi) and mi > threshold:
            #         G.add_edge(i, j, weight=mi)
    
    return G
