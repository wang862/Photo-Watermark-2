#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
模板管理模块
"""

import os
import json
import glob
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class TemplateManager:
    """模板管理器类，负责水印模板的保存、加载和管理"""
    
    def __init__(self, parent=None):
        """初始化模板管理器
        
        Args:
            parent: 父窗口对象，用于文件对话框和消息框
        """
        self.parent = parent
        self.templates_folder = self._get_default_templates_folder()
        self.template_extension = '.json'
        
    def _get_default_templates_folder(self):
        """获取默认的模板文件夹路径
        
        Returns:
            str: 模板文件夹路径
        """
        # 在用户目录下创建模板文件夹
        app_data_folder = os.path.join(os.path.expanduser("~"), "Photo-Watermark-2")
        templates_folder = os.path.join(app_data_folder, "templates")
        
        # 如果文件夹不存在，创建它
        if not os.path.exists(templates_folder):
            try:
                os.makedirs(templates_folder)
            except Exception:
                # 如果创建失败，使用当前工作目录
                templates_folder = os.path.join(os.getcwd(), "templates")
                if not os.path.exists(templates_folder):
                    try:
                        os.makedirs(templates_folder)
                    except Exception:
                        # 如果仍然失败，返回当前工作目录
                        templates_folder = os.getcwd()
        
        return templates_folder
        
    def save_template(self, template_name, template_data):
        """保存水印模板
        
        Args:
            template_name: 模板名称
            template_data: 模板数据字典
            
        Returns:
            bool: 是否保存成功
        """
        try:
            # 确保模板名称有效
            if not template_name or not isinstance(template_name, str):
                return False
            
            # 确保模板数据是字典
            if not isinstance(template_data, dict):
                return False
            
            # 为模板名称添加扩展名
            template_file_name = f"{template_name}{self.template_extension}"
            template_path = os.path.join(self.templates_folder, template_file_name)
            
            # 检查是否已存在同名模板
            if os.path.exists(template_path):
                reply = QMessageBox.question(
                    self.parent,
                    "确认覆盖",
                    f"模板 '{template_name}' 已存在，是否覆盖？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply != QMessageBox.Yes:
                    return False
            
            # 保存模板数据
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=4)
            
            return True
        except Exception:
            return False
            
    def load_template(self, template_name=None):
        """加载水印模板
        
        Args:
            template_name: 模板名称，如果为None则打开文件对话框让用户选择
            
        Returns:
            dict: 模板数据字典，如果加载失败则返回None
        """
        try:
            template_path = None
            
            if template_name:
                # 使用指定的模板名称
                template_file_name = f"{template_name}{self.template_extension}"
                template_path = os.path.join(self.templates_folder, template_file_name)
                
                if not os.path.exists(template_path):
                    # 模板不存在，让用户选择
                    template_path = None
            
            if not template_path:
                # 打开文件对话框让用户选择模板文件
                template_path, _ = QFileDialog.getOpenFileName(
                    self.parent,
                    "选择模板",
                    self.templates_folder,
                    f"模板文件 (*{self.template_extension})"
                )
                
                if not template_path:
                    return None
            
            # 加载模板数据
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            return template_data
        except Exception:
            return None
            
    def delete_template(self, template_name):
        """删除水印模板
        
        Args:
            template_name: 模板名称
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 构建模板文件路径
            template_file_name = f"{template_name}{self.template_extension}"
            template_path = os.path.join(self.templates_folder, template_file_name)
            
            # 检查模板是否存在
            if not os.path.exists(template_path):
                return False
            
            # 显示确认对话框
            reply = QMessageBox.question(
                self.parent,
                "确认删除",
                f"确定要删除模板 '{template_name}' 吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return False
            
            # 删除模板文件
            os.remove(template_path)
            
            return True
        except Exception:
            return False
            
    def get_all_templates(self):
        """获取所有可用的模板列表
        
        Returns:
            list: 模板名称列表
        """
        try:
            templates = []
            
            # 获取模板文件夹中的所有模板文件
            template_files = glob.glob(os.path.join(self.templates_folder, f"*{self.template_extension}"))
            
            # 提取模板名称
            for template_file in template_files:
                # 获取文件名（不带路径和扩展名）
                template_name = os.path.splitext(os.path.basename(template_file))[0]
                templates.append(template_name)
            
            # 按名称排序
            templates.sort()
            
            return templates
        except Exception:
            return []
            
    def rename_template(self, old_name, new_name):
        """重命名模板
        
        Args:
            old_name: 原模板名称
            new_name: 新模板名称
            
        Returns:
            bool: 是否重命名成功
        """
        try:
            # 构建原模板和新模板的文件路径
            old_file_name = f"{old_name}{self.template_extension}"
            new_file_name = f"{new_name}{self.template_extension}"
            
            old_path = os.path.join(self.templates_folder, old_file_name)
            new_path = os.path.join(self.templates_folder, new_file_name)
            
            # 检查原模板是否存在
            if not os.path.exists(old_path):
                return False
            
            # 检查新模板名称是否已存在
            if os.path.exists(new_path):
                reply = QMessageBox.question(
                    self.parent,
                    "确认覆盖",
                    f"模板 '{new_name}' 已存在，是否覆盖？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply != QMessageBox.Yes:
                    return False
            
            # 重命名文件
            os.rename(old_path, new_path)
            
            return True
        except Exception:
            return False
            
    def export_template(self, template_name, export_path):
        """导出模板
        
        Args:
            template_name: 模板名称
            export_path: 导出文件路径
            
        Returns:
            bool: 是否导出成功
        """
        try:
            # 构建模板文件路径
            template_file_name = f"{template_name}{self.template_extension}"
            template_path = os.path.join(self.templates_folder, template_file_name)
            
            # 检查模板是否存在
            if not os.path.exists(template_path):
                return False
            
            # 复制文件到导出路径
            import shutil
            shutil.copy2(template_path, export_path)
            
            return True
        except Exception:
            return False
            
    def import_template(self, import_path):
        """导入模板
        
        Args:
            import_path: 导入文件路径
            
        Returns:
            str: 导入的模板名称，如果导入失败则返回None
        """
        try:
            # 检查导入文件是否存在
            if not os.path.exists(import_path):
                return None
            
            # 检查文件是否为有效的JSON文件
            try:
                with open(import_path, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
            except Exception:
                return None
            
            # 获取文件名作为模板名称
            template_name = os.path.splitext(os.path.basename(import_path))[0]
            
            # 构建目标文件路径
            template_file_name = f"{template_name}{self.template_extension}"
            template_path = os.path.join(self.templates_folder, template_file_name)
            
            # 检查是否已存在同名模板
            if os.path.exists(template_path):
                reply = QMessageBox.question(
                    self.parent,
                    "确认覆盖",
                    f"模板 '{template_name}' 已存在，是否覆盖？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply != QMessageBox.Yes:
                    return None
            
            # 复制文件到模板文件夹
            import shutil
            shutil.copy2(import_path, template_path)
            
            return template_name
        except Exception:
            return None
            
    def get_template_folder(self):
        """获取模板文件夹路径
        
        Returns:
            str: 模板文件夹路径
        """
        return self.templates_folder
        
    def set_template_folder(self, folder_path):
        """设置模板文件夹路径
        
        Args:
            folder_path: 新的模板文件夹路径
            
        Returns:
            bool: 是否设置成功
        """
        try:
            # 检查文件夹是否存在
            if not os.path.exists(folder_path):
                # 尝试创建文件夹
                try:
                    os.makedirs(folder_path)
                except Exception:
                    return False
            
            # 检查是否有权限
            if not os.access(folder_path, os.W_OK):
                return False
            
            # 设置新的模板文件夹
            self.templates_folder = folder_path
            
            return True
        except Exception:
            return False