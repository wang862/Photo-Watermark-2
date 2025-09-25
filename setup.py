#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
安装配置文件
"""

from setuptools import setup, find_packages
import os

# 获取项目版本
version = "1.0.0"

# 获取长描述（从README.md读取）
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# 获取依赖列表（从requirements.txt读取）
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

# 定义项目资源
package_data = {
    "": ["*.txt", "*.md", "*.json"],
    "src.resources.icons": ["*.svg", "*.png", "*.ico"]
}

# 设置入口点
entry_points = {
    "console_scripts": [
        "photo-watermark=src.main.main:main",
    ],
    "gui_scripts": [
        "PhotoWatermark=src.main.main:main",
    ]
}

# 定义setup配置
setup(
    name="Photo-Watermark-2",
    version=version,
    author="PhotoWatermarkDev",
    author_email="developer@photowatermark.com",
    description="一个用于给图片添加水印的Windows工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PhotoWatermarkDev/Photo-Watermark-2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data=package_data,
    install_requires=requirements,
    entry_points=entry_points,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    keywords="photo, watermark, image processing, utility",
    project_urls={
        "Bug Reports": "https://github.com/PhotoWatermarkDev/Photo-Watermark-2/issues",
        "Source": "https://github.com/PhotoWatermarkDev/Photo-Watermark-2",
    },
    # Windows特定设置
    options={
        'build_exe': {
            'include_files': [
                ('src/resources/icons/app_icon.svg', 'icons/app_icon.svg'),
            ],
            'packages': ['PIL', 'PyQt5'],
            'excludes': ['tkinter'],
            'include_msvcr': True,
            'dist_dir': 'dist',
        }
    },
    # 数据文件
    data_files=[
        ('icons', ['src/resources/icons/app_icon.svg']),
    ],
)


# 以下是用于构建可执行文件的额外函数
if __name__ == "__main__":
    # 检查是否有构建可执行文件的参数
    import sys
    
    if len(sys.argv) > 1:
        # 支持通过命令行参数指定版本
        if sys.argv[1] == "--version" and len(sys.argv) == 3:
            version = sys.argv[2]
            sys.argv = sys.argv[:1]  # 移除自定义参数
            
        # 构建可执行文件
        if sys.argv[1] == "build_exe":
            try:
                from cx_Freeze import setup, Executable
                
                # 创建可执行文件配置
                executables = [
                    Executable(
                        "src/main/main.py",
                        base="Win32GUI",  # 使用GUI模式，不显示控制台窗口
                        targetName="PhotoWatermark.exe",
                        icon="src/resources/icons/app_icon.ico",  # 假设存在这个图标文件
                        shortcutName="Photo-Watermark-2",
                        shortcutDir="ProgramMenuFolder",
                    )
                ]
                
                # 设置cx_Freeze选项
                build_exe_options = {
                    "packages": ["os", "sys", "PIL", "PyQt5"],
                    "excludes": ["tkinter"],
                    "include_files": [
                        ("src/resources/icons", "icons"),
                    ],
                    "include_msvcr": True,
                    "optimize": 2,
                }
                
                # 运行cx_Freeze的setup
                setup(
                    name="Photo-Watermark-2",
                    version=version,
                    description="一个用于给图片添加水印的Windows工具",
                    options={"build_exe": build_exe_options},
                    executables=executables,
                )
                
            except ImportError:
                print("需要安装cx_Freeze来构建可执行文件: pip install cx_Freeze")
                sys.exit(1)