#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
主程序入口
"""

import sys
import os

# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)
# 获取src目录的绝对路径
src_dir = os.path.dirname(os.path.dirname(current_file))
# 将src目录添加到Python路径
sys.path.append(src_dir)

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """主函数"""
    # 设置中文字体支持
    os.environ['QT_FONT_DPI'] = '96'
    
    # 创建应用程序实例
    app = QApplication(sys.argv)
    app.setApplicationName("Photo-Watermark-2")
    app.setApplicationVersion("1.0.0")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()