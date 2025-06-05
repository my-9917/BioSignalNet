import matplotlib.pyplot as plt
import numpy as np

def plot_entropy_curve(entropy_values, title="Multiscale Entropy Analysis", xlabel="Scale Factor", 
                       ylabel="Entropy", save_path=None, show=False, ax=None):
    """
    绘制熵随尺度变化的曲线
    
    参数:
    entropy_values (list): 不同尺度下的熵值列表
    title (str): 图表标题
    xlabel (str): x轴标签
    ylabel (str): y轴标签
    save_path (str): 保存路径，None表示不保存
    show (bool): 是否显示图表
    ax (matplotlib.axes.Axes): 可选，用于绘制在特定的axes上
    
    返回:
    matplotlib.axes.Axes: 绘制的轴对象
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    
    scales = list(range(1, len(entropy_values) + 1))
    ax.plot(scales, entropy_values, 'o-', linewidth=2, markersize=6)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(scales)
    ax.grid(True)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    elif ax is None:  # 如果是新创建的图且不显示，则关闭
        plt.close()
    
    return ax

def plot_entropy_comparison(entropy_dict, title="Entropy Comparison", 
                           xlabel="Scale Factor", ylabel="Entropy", 
                           save_path=None, show=False):
    """
    比较多个记录或通道的熵曲线
    
    参数:
    entropy_dict (dict): 键为记录/通道名称，值为熵值列表的字典
    title (str): 图表标题
    xlabel (str): x轴标签
    ylabel (str): y轴标签
    save_path (str): 保存路径，None表示不保存
    show (bool): 是否显示图表
    
    返回:
    matplotlib.figure.Figure: 图表对象
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for name, values in entropy_dict.items():
        # 确定有效的熵值范围 (排除NaN)
        valid_values = np.array(values)
        valid_indices = ~np.isnan(valid_values)
        if np.any(valid_indices):
            scales = np.array(range(1, len(values) + 1))[valid_indices]
            valid_values = valid_values[valid_indices]
            ax.plot(scales, valid_values, 'o-', linewidth=2, label=name)
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    # ax.legend()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig
