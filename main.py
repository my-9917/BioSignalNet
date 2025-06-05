"""
主程序入口点
"""
from utils.plotting_config import configure_matplotlib_fonts
configure_matplotlib_fonts() # 配置matplotlib字体

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
import datetime
warnings.filterwarnings('ignore')

# 导入项目模块
from preprocessing.edf_loader import load_edf
from utils.signal_processing import preprocess_signal
from entropy.mse import compute_mse
from network_analysis.construct_graph import construct_similarity_graph
from network_analysis.network_metrics import extract_network_metrics
from visualization.plot_entropy import plot_entropy_curve, plot_entropy_comparison
from visualization.plot_network import plot_network_graph, plot_network_metrics_comparison

# 导入配置
from config import *

def process_single_file(edf_path, max_samples=5000):
    """处理单个EDF文件"""
    file_name = os.path.basename(edf_path).split('.')[0]
    print(f"\n处理文件: {file_name}")
    
    # 加载EDF数据
    data, labels = load_edf(edf_path)
    if data is None:
        print(f"无法处理文件 {file_name}，跳过")
        return None
    
    # 选择前6个通道，或所有通道如果少于6个
    n_channels = min(6, data.shape[0])
    selected_data = data[:n_channels, :max_samples]
    selected_labels = labels[:n_channels] if labels else [f"Channel {i+1}" for i in range(n_channels)]
    
    print(f"选择 {n_channels} 个通道用于分析: {selected_labels}")
    print(f"每个通道使用 {selected_data.shape[1]} 个样本点")
    
    # 预处理每个通道的信号
    preprocessed_signals = []
    for i, signal in enumerate(selected_data):
        proc_signal = preprocess_signal(signal, LOW_FREQ, HIGH_FREQ, SAMPLING_RATE)
        preprocessed_signals.append(proc_signal)
    
    preprocessed_signals = np.array(preprocessed_signals)
    
    # 计算熵
    print("计算熵值...")
    mse_results = []
    
    for i, signal in enumerate(tqdm(preprocessed_signals, desc="熵分析")):
        # 计算多尺度样本熵
        mse = compute_mse(signal, MSE_MAX_SCALE, SAMPEN_M, SAMPEN_R_RATIO)
        mse_results.append(mse)
    
    # 构建网络并计算网络指标
    print("构建相似性网络...")
    G = construct_similarity_graph(preprocessed_signals, SIMILARITY_MEASURE, SIMILARITY_THRESHOLD)
    network_metrics = extract_network_metrics(G)
    
    print(f"网络指标: {network_metrics}")
    
    return {
        'signals': preprocessed_signals,
        'labels': selected_labels,
        'mse': mse_results,
        'network': G,
        'metrics': network_metrics
    }

def save_single_file_results(file_name, results, output_dir):
    """保存单个文件的分析结果"""
    # 创建文件特定的输出目录
    file_output_dir = os.path.join(output_dir, file_name)
    os.makedirs(file_output_dir, exist_ok=True)
    
    # 1. 为每个通道保存熵曲线
    for i, label in enumerate(results['labels']):
        # MSE曲线
        plot_entropy_curve(
            results['mse'][i],
            title=f"{file_name} - {label} - MSE",
            save_path=os.path.join(file_output_dir, f"{label}_mse.png"),
            show=SHOW_FIGURES
        )
    
    # 2. 保存网络图
    plot_network_graph(
        results['network'],
        title=f"{file_name} - Signal Similarity Network",
        save_path=os.path.join(file_output_dir, "network.png"),
        show=SHOW_FIGURES
    )

def create_timestamped_output_dir():
    """创建带时间戳的输出目录"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    timestamped_dir = os.path.join(OUTPUT_DIR, f"analysis_{timestamp}")
    os.makedirs(timestamped_dir, exist_ok=True)
    return timestamped_dir

def run_batch_analysis():
    """运行批量分析"""
    # 创建输出目录
    output_dir = create_timestamped_output_dir()
    
    # 获取所有EDF文件
    edf_files = glob.glob(os.path.join(DATA_DIR, "*.edf"))
    if not edf_files:
        print(f"在 {DATA_DIR} 中没有找到EDF文件")
        return
    
    # 处理每个文件
    all_results = {}
    for edf_file in edf_files:
        results = process_single_file(edf_file)
        if results:
            file_name = os.path.basename(edf_file).split('.')[0]
            all_results[file_name] = results
            save_single_file_results(file_name, results, output_dir)
    
    # 比较不同文件的结果
    if all_results:
        compare_results(all_results, output_dir)

def compare_results(all_results, output_dir):
    """比较不同文件的结果"""
    if not all_results:
        print("没有可比较的结果")
        return
    
    # 比较不同记录的网络指标
    network_metrics_dict = {file_name: results['metrics'] for file_name, results in all_results.items()}
    
    print("生成网络指标比较图...")
    plot_network_metrics_comparison(
        network_metrics_dict,
        title="Network Metrics Comparison",
        save_path=os.path.join(output_dir, "network_metrics_comparison.png"),
        show=SHOW_FIGURES
    )

if __name__ == "__main__":
    run_batch_analysis()
