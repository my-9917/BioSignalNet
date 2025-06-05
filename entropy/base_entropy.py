import numpy as np

# 尝试导入熵计算所需的库
try:
    import nolds
    HAS_NOLDS = True
except ImportError:
    HAS_NOLDS = False
    print("警告: nolds库未安装，样本熵计算将不可用。请使用pip安装: pip install nolds")

def calculate_sample_entropy(time_series, m=2, r_ratio=0.2):
    """
    计算时间序列的样本熵 (Sample Entropy)。
    
    参数:
    time_series (np.array): 一维时间序列
    m (int): 嵌入维度
    r_ratio (float): 容限因子比例
    
    返回:
    float: 样本熵值
    """
    if len(time_series) == 0:
        return np.nan
    r = r_ratio * np.std(time_series)
    if r == 0:
        return np.nan
        
    try:
        if HAS_NOLDS:
            return nolds.sampen(time_series, emb_dim=m, tolerance=r)
        else:
            print("无法计算样本熵: 请安装nolds库")
            return np.nan
    except Exception as e:
        return np.nan

def calculate_permutation_entropy(time_series, m=3, delay=1):
    """
    计算时间序列的排列熵 (Permutation Entropy)。
    
    参数:
    time_series (np.array): 一维时间序列
    m (int): 嵌入维度/阶数
    delay (int): 时间延迟
    
    返回:
    float: 排列熵值
    """
    if len(time_series) < m * delay:
        return np.nan
        
    try:
        if HAS_ANTROPY:
            return antropy.perm_entropy(time_series, order=m, delay=delay, normalize=True)
        else:
            print("无法计算排列熵: 请安装antropy库")
            return np.nan
    except Exception as e:
        return np.nan

def calculate_fuzzy_entropy(time_series, m=2, r_ratio=0.2, n_fuzzy=2):
    """
    计算时间序列的模糊熵 (Fuzzy Entropy)。
    
    参数:
    time_series (np.array): 一维时间序列
    m (int): 嵌入维度
    r_ratio (float): 容限因子比例
    n_fuzzy (int): 模糊函数的指数
    
    返回:
    float: 模糊熵值
    """
    if len(time_series) < 2 * m:
        return np.nan
        
    r = r_ratio * np.std(time_series)
    if r == 0:
        return np.nan
        
    try:
        if HAS_ANTROPY:
            return antropy.fuzzy_entropy(time_series, order=m, r=r, n=n_fuzzy)
        else:
            print("无法计算模糊熵: 请安装antropy库")
            return np.nan
    except Exception as e:
        return np.nan
