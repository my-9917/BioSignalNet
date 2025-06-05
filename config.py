"""
全局配置文件
"""

# 数据参数
DATA_DIR = "data/adfecgdb/"  # 数据目录路径
OUTPUT_DIR = "output"  # 输出目录路径

# 熵计算参数
SAMPEN_M = 2  # 嵌入维度
SAMPEN_R_RATIO = 0.2  # 容限因子比例
MSE_MAX_SCALE = 20  # 最大尺度因子

# 网络分析参数
SIMILARITY_THRESHOLD = 0.5  # 相似度阈值，低于此值的边将被过滤
SIMILARITY_MEASURE = "correlation"  # 相似度计算方法

# 信号预处理参数
LOW_FREQ = 0.5  # 低通滤波截止频率
HIGH_FREQ = 45.0  # 高通滤波截止频率
SAMPLING_RATE = 256  # 采样率

# 可视化参数
SAVE_FIGURES = True  # 是否保存图表
SHOW_FIGURES = False  # 是否显示图表
DPI = 300  # 图表DPI
