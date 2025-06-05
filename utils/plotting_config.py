"""
配置Matplotlib以支持中文显示
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import platform

def configure_matplotlib_fonts():
    """配置Matplotlib支持中文显示"""
    system = platform.system()
    
    # 检测操作系统类型并设置合适的中文字体
    if system == 'Windows':
        font_family = ['Microsoft YaHei', 'SimHei']
    elif system == 'Darwin':  # macOS
        font_family = ['Heiti SC', 'Hiragino Sans GB', 'STHeiti']
    else:  # Linux和其他系统
        font_family = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'Droid Sans Fallback']
    
    # 寻找可用的字体
    font = None
    for f in font_family:
        try:
            # 检查字体是否存在
            from matplotlib.font_manager import FontProperties
            FontProperties(family=f)
            font = f
            print(f"使用字体: {font}")
            break
        except:
            continue
    
    if font is None:
        print("警告: 未找到合适的中文字体，将使用系统默认字体")
        # 可以尝试获取当前默认字体
        default_font = mpl.rcParams['font.family']
        print(f"当前默认字体: {default_font}")
        
        # 尝试使用更通用的设置
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica', 'sans-serif']
    else:
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = [font] + plt.rcParams['font.sans-serif']
    
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False
    
    # 设置全局字体大小
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    
    # 如果用户想要临时检查可用字体，可以使用以下代码：
    # from matplotlib.font_manager import findfont, FontProperties
    # print(findfont(FontProperties(family=['sans-serif'])))
