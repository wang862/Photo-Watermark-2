#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
图片列表组件
"""

from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QSize
import os
import io

from core.image_processor import ImageProcessor


class ImageListWidget(QListWidget):
    """图片列表组件"""
    
    def __init__(self, parent=None):
        """初始化图片列表"""
        super().__init__(parent)
        
        # 设置窗口属性
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(80, 80))
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSelectionMode(QListWidget.SingleSelection)
        
        # 设置样式
        self.setStyleSheet("background-color: #ffffff; border: 1px solid #cccccc;")
        
        # 存储父窗口引用
        self.parent = parent
        
        # 添加右键菜单支持
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # 创建删除按钮
        self.delete_button = QPushButton("删除所选图片")
        self.delete_button.clicked.connect(self.delete_selected_image)
        
    def add_image(self, file_path):
        """添加图片到列表
        
        Args:
            file_path: 图片文件路径
        """
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return False
            
        # 创建列表项
        item = QListWidgetItem()
        
        # 设置项目数据
        item.setData(Qt.UserRole, file_path)
        
        # 获取文件名
        file_name = os.path.basename(file_path)
        
        # 创建缩略图
        try:
            image_processor = ImageProcessor()
            # 使用正确的方法名get_image_thumbnail，参数是file_path和(max_width, max_height)
            pil_thumbnail = image_processor.get_image_thumbnail(file_path, (80, 80))
            
            if pil_thumbnail:
                # 将PIL图像转换为QPixmap
                img_byte_arr = io.BytesIO()
                pil_thumbnail.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                qimage = QImage.fromData(img_byte_arr.read())
                thumbnail = QPixmap.fromImage(qimage)
                
                # 创建自定义列表项
                custom_widget = self._create_custom_item_widget(file_name, thumbnail)
                
                # 设置项目大小
                item.setSizeHint(custom_widget.sizeHint())
                
                # 添加到列表
                self.addItem(item)
                self.setItemWidget(item, custom_widget)
                
                return True
            else:
                return False
        except Exception as e:
            print(f"创建缩略图失败: {str(e)}")
            return False
            
    def _create_custom_item_widget(self, file_name, thumbnail):
        """创建自定义列表项小部件
        
        Args:
            file_name: 文件名
            thumbnail: 缩略图QPixmap对象
        
        Returns:
            自定义小部件
        """
        # 创建小部件和布局
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        # 创建图片标签
        image_label = QLabel()
        image_label.setPixmap(thumbnail)
        image_label.setAlignment(Qt.AlignCenter)
        
        # 创建文件名标签
        name_label = QLabel(file_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setMaximumWidth(80)
        
        # 添加到布局
        layout.addWidget(image_label)
        layout.addWidget(name_label)
        
        return widget
        
    def delete_selected_image(self):
        """删除选中的图片"""
        current_item = self.currentItem()
        if current_item:
            # 获取图片路径
            file_path = current_item.data(Qt.UserRole)
            
            # 询问用户是否确认删除
            reply = QMessageBox.question(
                self.parent, "确认删除",
                f"确定要删除图片 '{os.path.basename(file_path)}' 吗？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # 从图片处理器中删除图片
                if hasattr(self.parent, 'image_processor'):
                    for i, path in enumerate(self.parent.image_processor.get_loaded_images()):
                        if path == file_path:
                            self.parent.image_processor.remove_image(i)
                            break
                
                # 从列表中删除项
                row = self.row(current_item)
                self.takeItem(row)
                
                # 如果删除后没有项目，清空预览
                if self.count() == 0:
                    if hasattr(self.parent, 'preview_widget'):
                        self.parent.preview_widget.clear()
                        
    def show_context_menu(self, position):
        """显示右键菜单
        
        Args:
            position: 右键点击位置
        """
        from PyQt5.QtWidgets import QMenu
        
        # 创建菜单
        menu = QMenu(self)
        
        # 添加删除操作
        delete_action = menu.addAction("删除")
        delete_action.triggered.connect(self.delete_selected_image)
        
        # 添加清除所有操作
        clear_all_action = menu.addAction("清除所有")
        clear_all_action.triggered.connect(self.clear_all_images)
        
        # 显示菜单
        menu.exec_(self.mapToGlobal(position))
        
    def clear_all_images(self):
        """清除所有图片"""
        # 询问用户是否确认删除
        reply = QMessageBox.question(
            self.parent, "确认清除",
            f"确定要清除所有 {self.count()} 张图片吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 清空图片处理器
            if hasattr(self.parent, 'image_processor'):
                self.parent.image_processor.clear_images()
            
            # 清空列表
            self.clear()
            
            # 清空预览
            if hasattr(self.parent, 'preview_widget'):
                self.parent.preview_widget.clear()
                
    def get_selected_image_path(self):
        """获取选中图片的路径
        
        Returns:
            选中图片的路径，如果没有选中则返回None
        """
        current_item = self.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None
        
    def get_all_image_paths(self):
        """获取所有图片的路径
        
        Returns:
            图片路径列表
        """
        paths = []
        for i in range(self.count()):
            item = self.item(i)
            if item:
                path = item.data(Qt.UserRole)
                if path:
                    paths.append(path)
        return paths
        
    def find_item_by_path(self, file_path):
        """通过路径查找列表项
        
        Args:
            file_path: 图片文件路径
        
        Returns:
            列表项，如果未找到则返回None
        """
        for i in range(self.count()):
            item = self.item(i)
            if item and item.data(Qt.UserRole) == file_path:
                return item
        return None