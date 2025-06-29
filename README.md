# 生理信号分析与网络构建

这个项目用于分析生理信号（如ECG、EEG等）并进行网络分析。主要功能包括信号预处理、多尺度熵分析和基于相关性的网络构建。

## 主要功能

1. 信号处理
   - EDF格式生理信号数据加载
   - 信号预处理（滤波、去噪）
   - 多通道信号分析

2. 熵分析
   - 多尺度样本熵 (MSE)
   - 支持自定义尺度因子和参数

3. 网络分析
   - 基于信号相关性的网络构建
   - 网络拓扑特征提取
   - 关键网络指标计算：
     - 网络密度
     - 平均度中心性
     - 同配性系数

4. 可视化
   - 熵值曲线绘制
   - 网络图可视化
   - 网络指标比较

## 安装依赖

必需依赖：
```bash
pip install numpy scipy matplotlib networkx mne tqdm nolds
```

## 使用方法

1. 准备数据
   - 将EDF格式的生理信号数据放在 `data/adfecgdb/` 目录下

2. 配置参数
   - 在 `config.py` 中调整相关参数：
     - 信号预处理参数（滤波频率、采样率等）
     - 熵计算参数（嵌入维度、容限因子等）
     - 网络构建参数（相似度阈值等）

3. 运行分析
   ```bash
   python main.py
   ```
   - 程序会自动处理所有EDF文件
   - 结果将保存在 `output/analysis_时间戳/` 目录下

## 输出说明

每个分析结果包含：
1. 每个通道的多尺度熵曲线
2. 信号相似性网络图
3. 网络指标比较图
4. 详细的指标汇总文本文件

## 项目结构

```
.
├── data/               # 数据目录
├── output/            # 输出目录
├── preprocessing/     # 信号预处理模块
├── entropy/          # 熵分析模块
├── network_analysis/ # 网络分析模块
├── visualization/    # 可视化模块
├── utils/            # 工具函数
├── config.py         # 配置文件
├── main.py           # 主程序
└── README.md         # 说明文档
```

## 注意事项

1. 信号预处理
   - 默认使用带通滤波（0.5-45Hz）
   - 采样率默认为256Hz

2. 网络构建
   - 使用相关系数作为相似度度量
   - 默认相似度阈值为0.5
   - 只保留强相关连接

3. 内存使用
   - 默认每个通道最多处理5000个样本点
   - 可以通过修改 `main.py` 中的 `max_samples` 参数调整
