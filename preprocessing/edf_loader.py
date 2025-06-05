import mne
import numpy as np
import os

def load_edf(edf_file_path):
    """
    加载EDF格式的ECG/EEG数据。
    
    参数:
    edf_file_path (str): EDF文件的完整路径
    
    返回:
    tuple: (数据数组, 通道标签)
    """
    try:
        raw = mne.io.read_raw_edf(edf_file_path, preload=True, verbose='WARNING')
        data = raw.get_data()
        labels = raw.ch_names
        print(f"成功加载文件: {edf_file_path}")
        print(f"数据形状: {data.shape}, 采样率: {raw.info['sfreq']} Hz")
        return data, labels
    except Exception as e:
        print(f"加载EDF文件 {edf_file_path} 失败: {e}")
        return None, None
