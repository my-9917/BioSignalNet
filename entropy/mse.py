import numpy as np
from .base_entropy import calculate_sample_entropy
from utils.signal_processing import coarse_grain_time_series

def compute_mse(signal, max_scale=20, m=2, r_ratio=0.2):
    """
    计算多尺度样本熵 (Multiscale Sample Entropy)
    
    参数:
    signal (np.array): 输入信号
    max_scale (int): 最大尺度因子
    m (int): 嵌入维度
    r_ratio (float): 容限因子比例
    
    返回:
    list: 不同尺度下的样本熵值
    """
    mse_values = []
    for scale in range(1, max_scale + 1):
        coarse_ts = coarse_grain_time_series(signal, scale)
        if len(coarse_ts) < 2 * m:
            mse_values.append(np.nan)
            continue
        sampen = calculate_sample_entropy(coarse_ts, m=m, r_ratio=r_ratio)
        mse_values.append(sampen)
    return mse_values
