#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
文件处理模块
"""

import os
import glob
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class FileHandler:
    """文件处理器类，负责文件的选择、保存等操作"""
    
    def __init__(self, parent=None):
        """初始化文件处理器
        
        Args:
            parent: 父窗口对象，用于文件对话框
        """
        self.parent = parent
        self.supported_formats = "Images (*.jpg *.jpeg *.png *.bmp)"
        
    def select_image(self):
        """选择单个图片文件
        
        Returns:
            str: 选择的图片文件路径，如果取消选择则返回None
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "选择图片",
            os.path.expanduser("~"),
            self.supported_formats
        )
        
        if file_path:
            return file_path
        return None
        
    def select_images(self):
        """选择多个图片文件
        
        Returns:
            list: 选择的图片文件路径列表，如果取消选择则返回空列表
        """
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.parent,
            "选择图片",
            os.path.expanduser("~"),
            self.supported_formats
        )
        
        return file_paths
        
    def select_folder(self):
        """选择文件夹
        
        Returns:
            str: 选择的文件夹路径，如果取消选择则返回None
        """
        folder_path = QFileDialog.getExistingDirectory(
            self.parent,
            "选择文件夹",
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder_path:
            return folder_path
        return None
        
    def select_output_folder(self, default_path=None):
        """选择输出文件夹
        
        Args:
            default_path: 默认文件夹路径
            
        Returns:
            str: 选择的输出文件夹路径，如果取消选择则返回None
        """
        folder_path = QFileDialog.getExistingDirectory(
            self.parent,
            "选择输出文件夹",
            default_path or os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder_path:
            return folder_path
        return None
        
    def get_save_file_path(self, default_name="watermarked", default_format="png"):
        """获取保存文件路径
        
        Args:
            default_name: 默认文件名
            default_format: 默认文件格式
            
        Returns:
            str: 保存文件路径，如果取消选择则返回None
        """
        # 根据默认格式设置文件过滤器
        if default_format.lower() == "jpg" or default_format.lower() == "jpeg":
            filter_str = "JPEG Image (*.jpg *.jpeg);;PNG Image (*.png)"
            default_suffix = "jpg"
        else:
            filter_str = "PNG Image (*.png);;JPEG Image (*.jpg *.jpeg)"
            default_suffix = "png"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent,
            "保存图片",
            os.path.join(os.path.expanduser("~"), f"{default_name}.{default_suffix}"),
            filter_str
        )
        
        if file_path:
            # 确保文件有扩展名
            ext = os.path.splitext(file_path)[1].lower()
            if not ext:
                file_path += f".{default_suffix}"
            return file_path
        return None
        
    def get_output_file_path(self, input_path, output_folder, naming_rule="original", prefix="", suffix=""):
        """根据命名规则生成输出文件路径
        
        Args:
            input_path: 输入文件路径
            output_folder: 输出文件夹路径
            naming_rule: 命名规则（original, prefix, suffix）
            prefix: 自定义前缀
            suffix: 自定义后缀
            
        Returns:
            str: 生成的输出文件路径
        """
        # 获取输入文件名和扩展名
        base_name = os.path.basename(input_path)
        name_without_ext, ext = os.path.splitext(base_name)
        
        # 根据命名规则生成新文件名
        if naming_rule == "prefix":
            new_name = f"{prefix}{name_without_ext}{ext}"
        elif naming_rule == "suffix":
            new_name = f"{name_without_ext}{suffix}{ext}"
        else:  # original
            new_name = base_name
        
        # 组合输出路径
        return os.path.join(output_folder, new_name)
        
    def is_safe_to_save(self, input_path, output_path):
        """检查保存是否安全（不会覆盖原图）
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            
        Returns:
            bool: 是否安全保存
        """
        # 规范化路径，不区分大小写
        input_path = os.path.normpath(input_path).lower()
        output_path = os.path.normpath(output_path).lower()
        
        # 检查是否是同一个文件
        if input_path == output_path:
            return False
        
        # 检查是否在同一个文件夹
        input_folder = os.path.dirname(input_path)
        output_folder = os.path.dirname(output_path)
        
        if input_folder == output_folder:
            # 如果在同一个文件夹，显示警告
            reply = QMessageBox.warning(
                self.parent,
                "警告",
                "输出文件夹与源文件文件夹相同，可能会覆盖现有文件。是否继续？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            return reply == QMessageBox.Yes
        
        return True
        
    def get_files_in_folder(self, folder_path, recursive=False):
        """获取文件夹中的所有图片文件
        
        Args:
            folder_path: 文件夹路径
            recursive: 是否递归搜索子文件夹
            
        Returns:
            list: 图片文件路径列表
        """
        if not os.path.isdir(folder_path):
            return []
            
        file_paths = []
        # 获取所有支持的图片格式
        extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        
        if recursive:
            # 递归搜索
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        file_paths.append(os.path.join(root, file))
        else:
            # 只搜索当前文件夹
            for ext in extensions:
                file_paths.extend(glob.glob(os.path.join(folder_path, f"*{ext}")))
                file_paths.extend(glob.glob(os.path.join(folder_path, f"*{ext.upper()}")))
        
        return file_paths
        
    def create_folder_if_not_exists(self, folder_path):
        """如果文件夹不存在则创建
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            bool: 是否创建成功或已存在
        """
        try:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            return True
        except Exception:
            return False
        
    def get_file_name_without_ext(self, file_path):
        """获取不带扩展名的文件名
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 不带扩展名的文件名
        """
        return os.path.splitext(os.path.basename(file_path))[0]
        
    def get_file_extension(self, file_path):
        """获取文件扩展名
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件扩展名（小写，带点）
        """
        return os.path.splitext(file_path)[1].lower()