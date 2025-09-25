#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
通用工具函数模块
"""

import os
import sys
import time
import datetime
import shutil
import hashlib
import re
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


def get_application_path():
    """获取应用程序路径
    
    Returns:
        应用程序路径
    """
    if getattr(sys, 'frozen', False):
        # 打包后的可执行文件
        return os.path.dirname(sys.executable)
    else:
        # 开发环境
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        

def get_resource_path(relative_path):
    """获取资源文件路径
    
    Args:
        relative_path: 相对路径
    
    Returns:
        绝对路径
    """
    base_path = get_application_path()
    return os.path.join(base_path, "src", "resources", relative_path)
    

def get_config_path(file_name):
    """获取配置文件路径
    
    Args:
        file_name: 文件名
    
    Returns:
        配置文件路径
    """
    if sys.platform == 'win32':
        appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
        config_dir = os.path.join(appdata, "PhotoWatermark")
    else:
        config_dir = os.path.join(os.path.expanduser('~'), ".PhotoWatermark")
        
    # 确保配置目录存在
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        
    return os.path.join(config_dir, file_name)
    

def get_current_time_str(format_str="%Y-%m-%d %H:%M:%S"):
    """获取当前时间字符串
    
    Args:
        format_str: 时间格式字符串
    
    Returns:
        格式化的时间字符串
    """
    return datetime.datetime.now().strftime(format_str)
    

def create_unique_filename(base_dir, base_name, extension):
    """创建唯一的文件名
    
    Args:
        base_dir: 基础目录
        base_name: 基础文件名
        extension: 文件扩展名
    
    Returns:
        唯一的文件路径
    """
    # 确保扩展名以.开头
    if not extension.startswith("."):
        extension = f".{extension}"
        
    # 构建初始文件路径
    file_path = os.path.join(base_dir, f"{base_name}{extension}")
    
    # 如果文件已存在，添加时间戳或序号
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(base_dir, f"{base_name}_{counter}{extension}")
        counter += 1
        
    return file_path
    

def sanitize_filename(filename):
    """清理文件名，移除非法字符
    
    Args:
        filename: 原始文件名
    
    Returns:
        清理后的文件名
    """
    # 根据操作系统移除非法字符
    if sys.platform == 'win32':
        # Windows系统非法字符
        invalid_chars = '<>:"/\\|?*'
    else:
        # 其他系统（Linux/Mac）
        invalid_chars = '/'  # 在Unix系统中，/是路径分隔符
        
    # 替换非法字符为下划线
    sanitized = "".join(c if c not in invalid_chars else "_" for c in filename)
    
    # 移除控制字符
    sanitized = re.sub(r'[\x00-\x1f\x7f]', '', sanitized)
    
    # 移除首尾空格
    sanitized = sanitized.strip()
    
    # 确保文件名不为空
    if not sanitized:
        sanitized = "unnamed"
        
    return sanitized
    

def calculate_file_hash(file_path, hash_type="md5"):
    """计算文件哈希值
    
    Args:
        file_path: 文件路径
        hash_type: 哈希算法类型（md5、sha1、sha256等）
    
    Returns:
        文件哈希值字符串
    """
    if not os.path.exists(file_path):
        return None
        
    # 创建哈希对象
    hash_obj = hashlib.new(hash_type)
    
    # 读取文件并计算哈希值
    try:
        with open(file_path, "rb") as f:
            # 分块读取文件
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
    except Exception as e:
        print(f"计算文件哈希值失败: {str(e)}")
        return None
        
    # 返回十六进制表示的哈希值
    return hash_obj.hexdigest()
    

def is_image_file(file_path):
    """检查文件是否为支持的图片格式
    
    Args:
        file_path: 文件路径
    
    Returns:
        是否为支持的图片格式
    """
    # 支持的图片扩展名
    supported_extensions = {
        ".jpg", ".jpeg", ".png", ".bmp", ".gif", 
        ".tiff", ".webp", ".svg"
    }
    
    # 获取文件扩展名并转换为小写
    _, ext = os.path.splitext(file_path.lower())
    
    return ext in supported_extensions
    

def create_directory(dir_path):
    """创建目录，如果不存在
    
    Args:
        dir_path: 目录路径
    
    Returns:
        是否创建成功
    """
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
            return True
        except Exception as e:
            print(f"创建目录失败: {str(e)}")
            return False
    return True
    

def copy_file(source_path, destination_path, overwrite=False):
    """复制文件
    
    Args:
        source_path: 源文件路径
        destination_path: 目标文件路径
        overwrite: 是否覆盖已存在的文件
    
    Returns:
        是否复制成功
    """
    # 检查源文件是否存在
    if not os.path.exists(source_path):
        print(f"源文件不存在: {source_path}")
        return False
        
    # 检查目标文件是否已存在
    if os.path.exists(destination_path) and not overwrite:
        print(f"目标文件已存在且不允许覆盖: {destination_path}")
        return False
        
    try:
        # 确保目标目录存在
        create_directory(os.path.dirname(destination_path))
        
        # 复制文件
        shutil.copy2(source_path, destination_path)
        return True
    except Exception as e:
        print(f"复制文件失败: {str(e)}")
        return False
        

def resize_image_keep_aspect_ratio(image, max_width, max_height):
    """调整图片大小，保持宽高比
    
    Args:
        image: QImage或QPixmap对象
        max_width: 最大宽度
        max_height: 最大高度
    
    Returns:
        调整大小后的图片对象
    """
    # 检查输入类型
    if isinstance(image, QPixmap):
        # 对于QPixmap
        return image.scaled(
            max_width, max_height,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
    elif isinstance(image, QImage):
        # 对于QImage
        return image.scaled(
            max_width, max_height,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
    else:
        # 不支持的类型
        return None
        

def get_file_size_formatted(file_path):
    """获取格式化的文件大小
    
    Args:
        file_path: 文件路径
    
    Returns:
        格式化的文件大小字符串
    """
    if not os.path.exists(file_path):
        return "文件不存在"
        
    # 获取文件大小（字节）
    file_size = os.path.getsize(file_path)
    
    # 转换为合适的单位
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    
    while file_size >= 1024 and unit_index < len(units) - 1:
        file_size /= 1024
        unit_index += 1
        
    # 格式化输出
    if unit_index == 0:
        return f"{int(file_size)} {units[unit_index]}"
    else:
        return f"{file_size:.2f} {units[unit_index]}"
        

def get_image_dimensions(file_path):
    """获取图片的尺寸
    
    Args:
        file_path: 图片文件路径
    
    Returns:
        (宽度, 高度)元组，如果获取失败则返回None
    """
    if not is_image_file(file_path):
        return None
        
    try:
        # 尝试加载图片
        image = QImage(file_path)
        if image.isNull():
            # 如果QImage加载失败，尝试QPixmap
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                return None
            return (pixmap.width(), pixmap.height())
        return (image.width(), image.height())
    except Exception as e:
        print(f"获取图片尺寸失败: {str(e)}")
        return None
        

# 用于测试的示例代码
if __name__ == "__main__":
    # 测试获取应用程序路径
    app_path = get_application_path()
    print(f"应用程序路径: {app_path}")
    
    # 测试获取资源路径
    resource_path = get_resource_path("icons/app_icon.png")
    print(f"资源路径: {resource_path}")
    
    # 测试获取当前时间
    current_time = get_current_time_str()
    print(f"当前时间: {current_time}")
    
    # 测试创建唯一文件名
    unique_name = create_unique_filename(".", "test", ".txt")
    print(f"唯一文件名: {unique_name}")
    
    # 测试清理文件名
    sanitized = sanitize_filename("test/..<file.txt")
    print(f"清理后的文件名: {sanitized}")