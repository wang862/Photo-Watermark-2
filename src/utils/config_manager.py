#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
配置管理模块
"""

import json
import os
import sys
from PyQt5.QtCore import QSettings


class ConfigManager:
    """配置管理器类，用于保存和加载用户配置"""
    
    def __init__(self, app_name="PhotoWatermark", company_name="PhotoWatermarkDev"):
        """初始化配置管理器
        
        Args:
            app_name: 应用程序名称，用于QSettings存储
            company_name: 公司名称，用于QSettings存储
        """
        # 使用QSettings进行配置存储
        self.settings = QSettings(company_name, app_name)
        
        # 默认配置
        self.default_config = {
            "output_folder": "",
            "export_format": "PNG",
            "naming_rule": "original",
            "prefix": "",
            "suffix": "",
            "last_template_folder": "",
            "recent_files": [],
            "window_size": (1024, 768),
            "window_position": (0, 0),
            "window_maximized": False
        }
        
        # 确保配置文件目录存在
        self._ensure_config_dir_exists()
        
    def _ensure_config_dir_exists(self):
        """确保配置文件目录存在"""
        # 对于QSettings，通常不需要手动创建目录，因为它会自动处理
        pass
        
    def save_setting(self, key, value):
        """保存单个设置
        
        Args:
            key: 设置键
            value: 设置值
        """
        self.settings.setValue(key, value)
        
    def load_setting(self, key, default_value=None):
        """加载单个设置
        
        Args:
            key: 设置键
            default_value: 默认值，如果设置不存在则返回
        
        Returns:
            设置值或默认值
        """
        if default_value is None:
            default_value = self.default_config.get(key, None)
            
        value = self.settings.value(key, default_value)
        
        # 类型转换，因为QSettings会将一些类型转换为字符串
        if key == "window_size" and isinstance(value, str):
            try:
                # 从字符串转换回元组
                import ast
                value = ast.literal_eval(value)
            except:
                value = default_value
        elif key == "window_position" and isinstance(value, str):
            try:
                import ast
                value = ast.literal_eval(value)
            except:
                value = default_value
        elif key == "window_maximized" and isinstance(value, str):
            value = value.lower() == "true"
        
        return value
        
    def save_all_settings(self, settings_dict):
        """保存所有设置
        
        Args:
            settings_dict: 设置字典
        """
        for key, value in settings_dict.items():
            self.save_setting(key, value)
            
    def load_all_settings(self):
        """加载所有设置
        
        Returns:
            设置字典
        """
        settings_dict = {}
        for key in self.default_config.keys():
            settings_dict[key] = self.load_setting(key)
        return settings_dict
        
    def reset_settings(self):
        """重置所有设置到默认值"""
        self.save_all_settings(self.default_config)
        
    def save_window_geometry(self, window):
        """保存窗口几何信息
        
        Args:
            window: QMainWindow对象
        """
        # 保存窗口位置和大小
        self.save_setting("window_size", window.size().width())
        self.save_setting("window_size", window.size().height())
        self.save_setting("window_position", (window.pos().x(), window.pos().y()))
        self.save_setting("window_maximized", window.isMaximized())
        
    def load_window_geometry(self, window):
        """加载窗口几何信息
        
        Args:
            window: QMainWindow对象
        """
        # 加载窗口位置和大小
        size = self.load_setting("window_size")
        position = self.load_setting("window_position")
        maximized = self.load_setting("window_maximized")
        
        if isinstance(size, tuple) and len(size) == 2:
            window.resize(size[0], size[1])
        elif isinstance(size, int):
            # 旧版本的兼容性处理
            pass
            
        if isinstance(position, tuple) and len(position) == 2:
            window.move(position[0], position[1])
            
        if maximized:
            window.showMaximized()
        
    def add_recent_file(self, file_path):
        """添加最近使用的文件
        
        Args:
            file_path: 文件路径
        """
        recent_files = self.load_setting("recent_files", [])
        
        # 如果文件已经在列表中，先移除
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # 添加到列表开头
        recent_files.insert(0, file_path)
        
        # 限制最近文件列表的大小
        max_recent = 10
        recent_files = recent_files[:max_recent]
        
        # 保存列表
        self.save_setting("recent_files", recent_files)
        
    def get_recent_files(self):
        """获取最近使用的文件列表
        
        Returns:
            最近文件列表
        """
        recent_files = self.load_setting("recent_files", [])
        
        # 过滤掉不存在的文件
        existing_files = []
        for file_path in recent_files:
            if os.path.exists(file_path):
                existing_files.append(file_path)
        
        # 如果过滤后的列表与原列表不同，更新设置
        if existing_files != recent_files:
            self.save_setting("recent_files", existing_files)
            
        return existing_files
        

# 用于测试的示例代码
if __name__ == "__main__":
    # 创建配置管理器实例
    config = ConfigManager()
    
    # 测试保存设置
    config.save_setting("output_folder", "C:\\Users\\User\\Desktop\\Output")
    config.save_setting("export_format", "JPEG")
    
    # 测试加载设置
    output_folder = config.load_setting("output_folder")
    export_format = config.load_setting("export_format")
    
    print(f"Output Folder: {output_folder}")
    print(f"Export Format: {export_format}")
    
    # 测试最近文件功能
    config.add_recent_file("C:\\Users\\User\\Desktop\\test1.jpg")
    config.add_recent_file("C:\\Users\\User\\Desktop\\test2.jpg")
    
    recent_files = config.get_recent_files()
    print(f"Recent Files: {recent_files}")