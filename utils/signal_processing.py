import numpy as np
from scipy import signal  # 使用signal而不是stats来获取detrend函数

def preprocess_signal(signal_data, low_freq=0.5, high_freq=45.0, sampling_rate=256):
    """
    对信号进行预处理，包括滤波等操作
    
    参数:
    signal_data (np.array): 原始信号数据
    low_freq (float): 低通滤波截止频率
    high_freq (float): 高通滤波截止频率
    sampling_rate (float): 采样率
    
    返回:
    np.array: 处理后的信号
    """
    # 这里可以添加更多的预处理步骤，如去基线、滤波等
    # 简单示例: 标准化信号
    if len(signal_data) == 0:
        return np.array([])
        
    # 移除线性趋势
    detrended_signal = signal.detrend(signal_data)  # 从signal模块获取detrend
    
    # Z-score标准化
    normalized_signal = (detrended_signal - np.mean(detrended_signal)) / np.std(detrended_signal)
    
    return normalized_signal

def coarse_grain_time_series(time_series, scale_factor):
    """
    对时间序列进行粗粒化处理，用于多尺度熵。
    
    参数:
    time_series (np.array): 原始一维时间序列
    scale_factor (int): 尺度因子
    
    返回:
    np.array: 粗粒化后的时间序列
    """
    n = len(time_series)
    n_coarse = n // scale_factor
    if n_coarse == 0:
        return np.array([])
    coarse_grained_ts = np.zeros(n_coarse)
    for i in range(n_coarse):
        coarse_grained_ts[i] = np.mean(time_series[i*scale_factor:(i+1)*scale_factor])
    return coarse_grained_ts
