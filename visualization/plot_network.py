import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def plot_network_graph(G, title="Signal Similarity Network", node_color='skyblue', 
                      edge_color_by_weight=True, save_path=None, show=False, ax=None):
    """
    可视化网络图
    
    参数:
    G (networkx.Graph): 待可视化的网络
    title (str): 图表标题
    node_color (str): 节点颜色
    edge_color_by_weight (bool): 是否根据边的权重着色
    save_path (str): 保存路径，None表示不保存
    show (bool): 是否显示图表
    ax (matplotlib.axes.Axes): 可选，用于绘制在特定的axes上
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    
    # 判断网络是否为空
    if G.number_of_nodes() == 0:
        ax.text(0.5, 0.5, "Empty Graph", ha='center', va='center', fontsize=14)
        ax.axis('off')
        return ax
    
    # 获取节点位置 - 使用spring布局
    pos = nx.spring_layout(G, seed=42)  # 固定seed以便结果可复现
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=500, alpha=0.8, ax=ax)
    
    # 绘制节点标签
    nx.draw_networkx_labels(G, pos, font_color='black', font_weight='bold', ax=ax)
    
    # 绘制边
    if edge_color_by_weight and nx.get_edge_attributes(G, 'weight'):
        edges = G.edges(data=True)
        weights = [data['weight'] for _, _, data in edges]
        norm = plt.Normalize(min(weights), max(weights))
        
        # 创建颜色映射
        cmap = plt.cm.Blues
        edge_colors = [cmap(norm(weight)) for weight in weights]
        
        # 绘制边，颜色由权重决定
        nx.draw_networkx_edges(G, pos, width=2, edge_color=edge_colors, alpha=0.7, ax=ax)
        
        # 添加颜色条
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        plt.colorbar(sm, ax=ax, label='Edge Weight')
    else:
        # 正常绘制边，不考虑权重
        nx.draw_networkx_edges(G, pos, width=2, edge_color='gray', alpha=0.7, ax=ax)
    
    ax.set_title(title)
    ax.axis('off')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    elif ax is None:  # 如果是新创建的图且不显示，则关闭
        plt.close()
    
    return ax

def plot_network_metrics_comparison(metrics_dict, metrics_to_plot=None, title="Network Metrics Comparison",
                                   save_path=None, show=False):
    """
    比较多个网络的指标
    
    参数:
    metrics_dict (dict): 键为网络名，值为网络指标字典的字典
    metrics_to_plot (list): 要绘制的指标名称列表，None表示全部
    title (str): 图表标题
    save_path (str): 保存路径，None表示不保存
    show (bool): 是否显示图表
    """
    if not metrics_dict:
        print("错误：metrics_dict为空")
        return None
    
    # 如果未指定要绘制的指标，则使用第一个网络的所有指标
    if metrics_to_plot is None:
        first_metrics = next(iter(metrics_dict.values()))
        metrics_to_plot = list(first_metrics.keys())
    
    # 限制只绘制通用指标，避免出错
    common_metrics = []
    for metric in metrics_to_plot:
        if all(metric in m for m in metrics_dict.values()):
            common_metrics.append(metric)
    
    if not common_metrics:
        print("警告: 找不到所有网络共有的指标")
        return None
    
    metrics_to_plot = common_metrics
    network_names = list(metrics_dict.keys())
    
    # 为每个指标创建单独的图表
    for metric in metrics_to_plot:
        try:
            plt.figure(figsize=(10, 6))
            
            # 获取指标值
            values = [metrics_dict[name].get(metric, np.nan) for name in network_names]
            
            # 绘制柱状图
            bars = plt.bar(range(len(network_names)), values, color='skyblue', alpha=0.7)
            
            # 添加数值标签
            for bar, value in zip(bars, values):
                if not np.isnan(value):
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                           f'{value:.4f}', ha='center', va='bottom', fontsize=9)
            
            # 设置标题和标签
            plt.title(f'Comparison of {metric}')
            plt.xticks(range(len(network_names)), network_names, rotation=45, ha='right')
            plt.ylabel(metric)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # 保存图表
            if save_path:
                metric_save_path = save_path.replace('.png', f'_{metric}.png')
                plt.savefig(metric_save_path, dpi=100)
            
            if show:
                plt.show()
            else:
                plt.close()
                
        except Exception as e:
            print(f"绘制指标 {metric} 时出错: {e}")
    
    # 创建汇总信息的文本文件
    if save_path:
        try:
            summary_path = save_path.replace('.png', '_summary.txt')
            with open(summary_path, 'w') as f:
                f.write(f"Network Metrics Comparison Summary\n")
                f.write(f"================================\n\n")
                
                for name in network_names:
                    f.write(f"Network: {name}\n")
                    for metric in metrics_to_plot:
                        value = metrics_dict[name].get(metric, np.nan)
                        f.write(f"  {metric}: {value:.6f}\n")
                    f.write("\n")
        except Exception as e:
            print(f"创建汇总文件时出错: {e}")
