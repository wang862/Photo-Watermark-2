#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
构建可执行文件脚本
"""

import sys
import os
from cx_Freeze import setup, Executable

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 设置版本号
version = "1.0.0"

# 创建可执行文件配置
executables = [
    Executable(
        os.path.join(current_dir, "src", "main", "main.py"),
        base="Win32GUI",  # 使用GUI模式，不显示控制台窗口
        target_name="PhotoWatermark.exe",
        icon=os.path.join(current_dir, "src", "resources", "icons", "app_icon.svg"),
        shortcut_name="Photo-Watermark-2",
        shortcut_dir="ProgramMenuFolder",
    )
]

# 设置cx_Freeze选项
build_exe_options = {
    "packages": ["os", "sys", "PIL", "PyQt5"],
    "excludes": ["tkinter"],
    "include_files": [
        (os.path.join(current_dir, "src", "resources", "icons"), "icons"),
    ],
    "include_msvcr": True,
    "optimize": 2,
    "build_exe": os.path.join(current_dir, "dist"),
}

# 运行cx_Freeze的setup
setup(
    name="Photo-Watermark-2",
    version=version,
    description="一个用于给图片添加水印的Windows工具",
    options={"build_exe": build_exe_options},
    executables=executables,
)