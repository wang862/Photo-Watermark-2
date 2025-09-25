#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
主窗口模块
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QLabel,
    QPushButton, QLineEdit, QComboBox, QSlider, QGroupBox, QGridLayout,
    QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QColorDialog,
    QTabWidget, QSpinBox, QDoubleSpinBox, QCheckBox, QFontDialog, QProgressDialog
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QSize, QPoint, QRect

from core.image_processor import ImageProcessor
from core.watermark import Watermark
from core.file_handler import FileHandler
from core.template_manager import TemplateManager
from ui.preview_widget import PreviewWidget
from ui.image_list_widget import ImageListWidget


class MainWindow(QMainWindow):
    """主窗口类，包含整个应用程序的UI和逻辑"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        
        # 初始化核心组件
        self.image_processor = ImageProcessor()
        self.watermark = Watermark()
        self.file_handler = FileHandler(self)
        self.template_manager = TemplateManager(self)
        
        # 设置窗口属性
        self.setWindowTitle("Photo-Watermark-2")
        self.setMinimumSize(1024, 768)
        
        # 创建UI
        self.setup_ui()
        
        # 连接信号和槽
        self.connect_signals_slots()
        
        # 加载上次的设置
        self.load_settings()
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建左侧面板（图片列表）
        left_panel = QWidget()
        left_panel.setMaximumWidth(250)
        left_panel_layout = QVBoxLayout(left_panel)
        
        # 创建顶部按钮区域
        top_buttons_layout = QHBoxLayout()
        
        self.import_button = QPushButton("导入图片")
        self.import_folder_button = QPushButton("导入文件夹")
        
        top_buttons_layout.addWidget(self.import_button)
        top_buttons_layout.addWidget(self.import_folder_button)
        
        # 创建图片列表
        self.image_list_widget = ImageListWidget(self)
        
        left_panel_layout.addLayout(top_buttons_layout)
        left_panel_layout.addWidget(self.image_list_widget)
        
        # 创建主分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        
        # 创建右侧面板
        right_panel = QWidget()
        right_panel_layout = QVBoxLayout(right_panel)
        
        # 创建预览区域
        self.preview_widget = PreviewWidget(self)
        right_panel_layout.addWidget(self.preview_widget)
        
        # 创建设置选项卡
        self.tabs = QTabWidget()
        
        # 创建水印设置选项卡
        self.setup_watermark_tab()
        
        # 创建导出设置选项卡
        self.setup_export_tab()
        
        # 创建模板管理选项卡
        self.setup_template_tab()
        
        right_panel_layout.addWidget(self.tabs)
        
        # 添加右侧面板到分割器
        splitter.addWidget(right_panel)
        
        # 设置分割器的初始大小
        splitter.setSizes([250, 774])  # 左侧250，右侧774（总共1024）
        
        main_layout.addWidget(splitter)
        
    def setup_watermark_tab(self):
        """设置水印设置选项卡"""
        watermark_tab = QWidget()
        watermark_layout = QVBoxLayout(watermark_tab)
        
        # 文本水印设置
        text_group = QGroupBox("文本水印")
        text_layout = QVBoxLayout(text_group)
        
        self.watermark_text_edit = QLineEdit()
        self.watermark_text_edit.setPlaceholderText("输入水印文本")
        text_layout.addWidget(self.watermark_text_edit)
        
        # 字体设置
        font_layout = QHBoxLayout()
        
        self.font_name_label = QLabel("Arial")
        self.font_name_label.setMinimumWidth(100)
        self.font_button = QPushButton("选择字体")
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(8, 128)
        self.font_size_spinbox.setValue(24)
        self.font_size_label = QLabel("字号")
        
        font_layout.addWidget(self.font_size_label)
        font_layout.addWidget(self.font_size_spinbox)
        font_layout.addWidget(self.font_name_label)
        font_layout.addWidget(self.font_button)
        font_layout.addStretch()
        
        text_layout.addLayout(font_layout)
        
        # 样式设置
        style_layout = QHBoxLayout()
        
        self.bold_checkbox = QCheckBox("粗体")
        self.italic_checkbox = QCheckBox("斜体")
        
        style_layout.addWidget(self.bold_checkbox)
        style_layout.addWidget(self.italic_checkbox)
        style_layout.addStretch()
        
        text_layout.addLayout(style_layout)
        
        # 颜色和透明度设置
        color_layout = QHBoxLayout()
        
        self.color_button = QPushButton("选择颜色")
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(30, 20)
        self.color_preview.setStyleSheet("background-color: rgba(255, 255, 255, 128); border: 1px solid #ccc;")
        
        opacity_layout = QHBoxLayout()
        self.opacity_label = QLabel("50%")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(50)
        self.opacity_slider.setMinimumWidth(100)
        opacity_label_text = QLabel("透明度:")
        
        opacity_layout.addWidget(opacity_label_text)
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_label)
        
        color_layout.addWidget(self.color_button)
        color_layout.addWidget(self.color_preview)
        color_layout.addStretch()
        
        text_layout.addLayout(color_layout)
        text_layout.addLayout(opacity_layout)
        
        # 位置设置
        position_group = QGroupBox("位置设置")
        position_layout = QVBoxLayout(position_group)
        
        # 预设位置网格
        preset_position_layout = QGridLayout()
        
        positions = [
            ("左上", "top_left", 0, 0),
            ("中上", "top_center", 0, 1),
            ("右上", "top_right", 0, 2),
            ("左中", "middle_left", 1, 0),
            ("中心", "center", 1, 1),
            ("右中", "middle_right", 1, 2),
            ("左下", "bottom_left", 2, 0),
            ("中下", "bottom_center", 2, 1),
            ("右下", "bottom_right", 2, 2)
        ]
        
        self.position_buttons = {}
        for text, position, row, col in positions:
            button = QPushButton(text)
            button.setFixedSize(60, 30)
            button.setCheckable(True)
            if position == "center":
                button.setChecked(True)
            self.position_buttons[position] = button
            preset_position_layout.addWidget(button, row, col)
        
        # 旋转设置
        rotation_layout = QHBoxLayout()
        self.rotation_label = QLabel("0°")
        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setRange(-180, 180)
        self.rotation_slider.setValue(0)
        rotation_label_text = QLabel("旋转角度:")
        
        rotation_layout.addWidget(rotation_label_text)
        rotation_layout.addWidget(self.rotation_slider)
        rotation_layout.addWidget(self.rotation_label)
        
        position_layout.addLayout(preset_position_layout)
        position_layout.addLayout(rotation_layout)
        
        watermark_layout.addWidget(text_group)
        watermark_layout.addWidget(position_group)
        
        # 添加水印设置选项卡
        self.tabs.addTab(watermark_tab, "水印设置")
        
    def setup_export_tab(self):
        """设置导出设置选项卡"""
        export_tab = QWidget()
        export_layout = QVBoxLayout(export_tab)
        
        # 输出文件夹设置
        folder_layout = QHBoxLayout()
        
        self.output_folder_edit = QLineEdit()
        self.output_folder_edit.setPlaceholderText("选择输出文件夹")
        self.select_folder_button = QPushButton("浏览...")
        
        folder_layout.addWidget(self.output_folder_edit)
        folder_layout.addWidget(self.select_folder_button)
        
        # 输出格式设置
        format_layout = QHBoxLayout()
        
        format_label = QLabel("输出格式:")
        self.format_combobox = QComboBox()
        self.format_combobox.addItems(["PNG", "JPEG"])
        
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combobox)
        format_layout.addStretch()
        
        # 命名规则设置
        naming_group = QGroupBox("命名规则")
        naming_layout = QVBoxLayout(naming_group)
        
        self.naming_combobox = QComboBox()
        self.naming_combobox.addItems(["保留原文件名", "添加前缀", "添加后缀"])
        
        # 前缀和后缀输入
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText("输入前缀")
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setPlaceholderText("输入后缀")
        
        # 初始状态：保留原文件名，禁用前后缀输入框
        self.prefix_edit.setEnabled(False)
        self.suffix_edit.setEnabled(False)
        
        naming_layout.addWidget(self.naming_combobox)
        naming_layout.addWidget(self.prefix_edit)
        naming_layout.addWidget(self.suffix_edit)
        
        # 导出按钮
        self.export_button = QPushButton("导出图片")
        self.export_button.setMinimumHeight(40)
        
        export_layout.addWidget(QLabel("输出文件夹:"))
        export_layout.addLayout(folder_layout)
        export_layout.addLayout(format_layout)
        export_layout.addWidget(naming_group)
        export_layout.addWidget(self.export_button)
        export_layout.addStretch()
        
        # 添加导出设置选项卡
        self.tabs.addTab(export_tab, "导出设置")
        
    def setup_template_tab(self):
        """设置模板管理选项卡"""
        template_tab = QWidget()
        template_layout = QVBoxLayout(template_tab)
        
        # 模板列表
        self.template_list_widget = QListWidget()
        
        # 模板操作按钮
        template_buttons_layout = QHBoxLayout()
        
        self.save_template_button = QPushButton("保存模板")
        self.load_template_button = QPushButton("加载模板")
        self.delete_template_button = QPushButton("删除模板")
        
        template_buttons_layout.addWidget(self.save_template_button)
        template_buttons_layout.addWidget(self.load_template_button)
        template_buttons_layout.addWidget(self.delete_template_button)
        
        template_layout.addWidget(self.template_list_widget)
        template_layout.addLayout(template_buttons_layout)
        
        # 添加模板管理选项卡
        self.tabs.addTab(template_tab, "模板管理")
        
    def connect_signals_slots(self):
        """连接信号和槽"""
        # 文件操作信号
        self.import_button.clicked.connect(self.on_import_button_clicked)
        self.import_folder_button.clicked.connect(self.on_import_folder_button_clicked)
        self.select_folder_button.clicked.connect(self.on_select_folder_button_clicked)
        self.export_button.clicked.connect(self.on_export_button_clicked)
        
        # 水印设置信号
        self.watermark_text_edit.textChanged.connect(self.on_watermark_text_changed)
        self.font_button.clicked.connect(self.on_font_button_clicked)
        self.font_size_spinbox.valueChanged.connect(self.on_font_size_changed)
        self.bold_checkbox.stateChanged.connect(self.on_font_style_changed)
        self.italic_checkbox.stateChanged.connect(self.on_font_style_changed)
        self.color_button.clicked.connect(self.on_color_button_clicked)
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        self.rotation_slider.valueChanged.connect(self.on_rotation_changed)
        
        # 位置按钮信号
        for position, button in self.position_buttons.items():
            button.clicked.connect(lambda checked, pos=position: self.on_position_button_clicked(pos, checked))
        
        # 命名规则信号
        self.naming_combobox.currentIndexChanged.connect(self.on_naming_rule_changed)
        
        # 模板管理信号
        self.save_template_button.clicked.connect(self.on_save_template_button_clicked)
        self.load_template_button.clicked.connect(self.on_load_template_button_clicked)
        self.delete_template_button.clicked.connect(self.on_delete_template_button_clicked)
        self.template_list_widget.itemClicked.connect(self.on_template_item_clicked)
        
        # 图片列表信号
        self.image_list_widget.itemSelectionChanged.connect(self.on_image_selected)
        
        # 预览窗口信号
        # 这里需要在PreviewWidget类中定义信号
        
    def on_import_button_clicked(self):
        """导入图片按钮点击事件"""
        file_paths = self.file_handler.select_images()
        if file_paths:
            self.load_images(file_paths)
            
    def on_import_folder_button_clicked(self):
        """导入文件夹按钮点击事件"""
        folder_path = self.file_handler.select_folder()
        if folder_path:
            file_paths = self.file_handler.get_files_in_folder(folder_path)
            if file_paths:
                self.load_images(file_paths)
            else:
                QMessageBox.information(self, "提示", "所选文件夹中没有支持的图片文件")
                
    def load_images(self, file_paths):
        """加载图片到图片列表"""
        for file_path in file_paths:
            self.image_processor.load_image(file_path)
            self.image_list_widget.add_image(file_path)
            
        # 如果是第一次加载图片，选中第一张
        if self.image_list_widget.count() > 0 and not self.image_list_widget.currentItem():
            self.image_list_widget.setCurrentRow(0)
        
        # 更新预览
        self.update_preview()
        
    def on_image_selected(self):
        """图片列表选择事件"""
        current_item = self.image_list_widget.currentItem()
        if current_item:
            image_path = current_item.data(Qt.UserRole)
            # 设置当前图片
            for i, path in enumerate(self.image_processor.get_loaded_images()):
                if path == image_path:
                    self.image_processor.set_current_image(i)
                    break
            # 更新预览
            self.update_preview()
            
    def update_preview(self):
        """更新预览窗口"""
        current_image = self.image_processor.get_current_image()
        if current_image:
            # 获取水印设置
            watermark_text = self.watermark_text_edit.text()
            
            if watermark_text:
                # 应用水印设置
                self.watermark.set_text(watermark_text)
                
                # 添加水印到预览图片
                preview_image = self.watermark.add_watermark(
                    self.image_processor.get_loaded_images()[self.image_processor.current_image_index]
                )
                
                # 更新预览窗口
                self.preview_widget.set_image(preview_image)
            else:
                # 没有水印文本，直接显示原图
                self.preview_widget.set_image(current_image)
                
    def on_watermark_text_changed(self, text):
        """水印文本变化事件"""
        self.update_preview()
        
    def on_font_button_clicked(self):
        """字体选择按钮点击事件"""
        font, ok = QFontDialog.getFont(
            QFont(self.font_name_label.text(), self.font_size_spinbox.value()),
            self, "选择字体"
        )
        if ok:
            self.font_name_label.setText(font.family())
            self.font_size_spinbox.setValue(font.pointSize())
            self.bold_checkbox.setChecked(font.bold())
            self.italic_checkbox.setChecked(font.italic())
            self.update_preview()
            
    def on_font_size_changed(self, size):
        """字体大小变化事件"""
        self.update_preview()
        
    def on_font_style_changed(self):
        """字体样式变化事件"""
        self.update_preview()
        
    def on_color_button_clicked(self):
        """颜色选择按钮点击事件"""
        color = QColorDialog.getColor(Qt.white, self, "选择颜色")
        if color.isValid():
            # 设置颜色预览
            opacity = self.opacity_slider.value()
            self.color_preview.setStyleSheet(
                f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, {int(opacity * 2.55)}); border: 1px solid #ccc;"
            )
            # 更新水印颜色
            self.update_preview()
            
    def on_opacity_changed(self, value):
        """透明度变化事件"""
        self.opacity_label.setText(f"{value}%")
        # 更新颜色预览的透明度
        color = QColor()
        style_sheet = self.color_preview.styleSheet()
        # 从样式表中提取RGB值（简化处理）
        start = style_sheet.find("rgba(") + 5
        end = style_sheet.find(")", start)
        if start > 5 and end > start:
            rgba_values = style_sheet[start:end].split(",")
            if len(rgba_values) >= 3:
                r, g, b = map(int, rgba_values[:3])
                self.color_preview.setStyleSheet(
                    f"background-color: rgba({r}, {g}, {b}, {int(value * 2.55)}); border: 1px solid #ccc;"
                )
        self.update_preview()
        
    def on_rotation_changed(self, value):
        """旋转角度变化事件"""
        self.rotation_label.setText(f"{value}°")
        self.update_preview()
        
    def on_position_button_clicked(self, position, checked):
        """位置按钮点击事件"""
        if checked:
            # 取消其他按钮的选中状态
            for pos, button in self.position_buttons.items():
                if pos != position:
                    button.setChecked(False)
            # 更新水印位置
            self.watermark.set_position(position)
            self.update_preview()
            
    def on_naming_rule_changed(self, index):
        """命名规则变化事件"""
        if index == 1:  # 添加前缀
            self.prefix_edit.setEnabled(True)
            self.suffix_edit.setEnabled(False)
        elif index == 2:  # 添加后缀
            self.prefix_edit.setEnabled(False)
            self.suffix_edit.setEnabled(True)
        else:  # 保留原文件名
            self.prefix_edit.setEnabled(False)
            self.suffix_edit.setEnabled(False)
            
    def on_select_folder_button_clicked(self):
        """选择输出文件夹按钮点击事件"""
        folder_path = self.file_handler.select_output_folder(self.output_folder_edit.text())
        if folder_path:
            self.output_folder_edit.setText(folder_path)
            
    def on_export_button_clicked(self):
        """导出图片按钮点击事件"""
        # 检查是否有加载的图片
        loaded_images = self.image_processor.get_loaded_images()
        if not loaded_images:
            QMessageBox.warning(self, "警告", "没有可导出的图片")
            return
            
        # 检查是否设置了输出文件夹
        output_folder = self.output_folder_edit.text()
        if not output_folder:
            output_folder = self.file_handler.select_output_folder()
            if not output_folder:
                return
            self.output_folder_edit.setText(output_folder)
            
        # 确保输出文件夹存在
        if not self.file_handler.create_folder_if_not_exists(output_folder):
            QMessageBox.warning(self, "警告", "无法创建输出文件夹")
            return
            
        # 显示进度对话框
        progress = QProgressDialog("正在导出图片...", "取消", 0, len(loaded_images), self)
        progress.setWindowTitle("导出进度")
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(0)
        
        # 导出图片
        success_count = 0
        for i, image_path in enumerate(loaded_images):
            # 检查是否取消
            if progress.wasCanceled():
                break
                
            try:
                # 获取输出文件名
                naming_rule = "original"
                if self.naming_combobox.currentIndex() == 1:
                    naming_rule = "prefix"
                elif self.naming_combobox.currentIndex() == 2:
                    naming_rule = "suffix"
                
                # 获取文件扩展名
                ext = self.file_handler.get_file_extension(image_path)
                if self.format_combobox.currentText() == "PNG":
                    ext = ".png"
                else:
                    ext = ".jpg"
                
                # 根据命名规则生成输出文件路径
                output_path = self.file_handler.get_output_file_path(
                    image_path, 
                    output_folder, 
                    naming_rule, 
                    self.prefix_edit.text(), 
                    self.suffix_edit.text()
                )
                
                # 检查是否安全保存
                if not self.file_handler.is_safe_to_save(image_path, output_path):
                    continue
                    
                # 应用水印设置
                watermark_text = self.watermark_text_edit.text()
                if watermark_text:
                    # 设置水印文本
                    self.watermark.set_text(watermark_text)
                    
                    # 设置字体
                    font_name = self.font_name_label.text()
                    font_size = self.font_size_spinbox.value()
                    font_bold = self.bold_checkbox.isChecked()
                    font_italic = self.italic_checkbox.isChecked()
                    self.watermark.set_font(font_name, font_size, font_bold, font_italic)
                    
                    # 设置颜色和透明度
                    # 从样式表中提取RGB值（简化处理）
                    style_sheet = self.color_preview.styleSheet()
                    start = style_sheet.find("rgba(") + 5
                    end = style_sheet.find(")", start)
                    if start > 5 and end > start:
                        rgba_values = style_sheet[start:end].split(",")
                        if len(rgba_values) >= 3:
                            r, g, b = map(int, rgba_values[:3])
                            opacity = self.opacity_slider.value()
                            self.watermark.set_color(r, g, b, opacity)
                    
                    # 设置位置
                    for pos, button in self.position_buttons.items():
                        if button.isChecked():
                            self.watermark.set_position(pos)
                            break
                    
                    # 设置旋转角度
                    rotation = self.rotation_slider.value()
                    self.watermark.set_rotation(rotation)
                    
                    # 添加水印并保存
                    self.watermark.add_watermark(image_path, output_path)
                    success_count += 1
                
            except Exception as e:
                QMessageBox.warning(self, "导出失败", f"导出 {os.path.basename(image_path)} 时出错: {str(e)}")
                
            # 更新进度
            progress.setValue(i + 1)
            
        # 显示导出结果
        if success_count > 0:
            QMessageBox.information(self, "导出完成", f"成功导出 {success_count} 张图片到 {output_folder}")
        elif progress.wasCanceled():
            QMessageBox.information(self, "导出取消", "导出操作已取消")
        else:
            QMessageBox.warning(self, "导出失败", "没有成功导出任何图片")
            
    def on_save_template_button_clicked(self):
        """保存模板按钮点击事件"""
        # 获取当前水印设置
        template_data = {
            "text": self.watermark_text_edit.text(),
            "font_name": self.font_name_label.text(),
            "font_size": self.font_size_spinbox.value(),
            "font_bold": self.bold_checkbox.isChecked(),
            "font_italic": self.italic_checkbox.isChecked(),
            # 从样式表中提取颜色值（简化处理）
            "color": self._get_color_from_preview(),
            "opacity": self.opacity_slider.value(),
            # 获取选中的位置
            "position": self._get_selected_position(),
            "rotation": self.rotation_slider.value()
        }
        
        # 获取模板名称
        from PyQt5.QtWidgets import QInputDialog
        template_name, ok = QInputDialog.getText(self, "保存模板", "请输入模板名称:")
        
        if ok and template_name:
            # 保存模板
            if self.template_manager.save_template(template_name, template_data):
                # 更新模板列表
                self.update_template_list()
                QMessageBox.information(self, "保存成功", f"模板 '{template_name}' 已保存")
            else:
                QMessageBox.warning(self, "保存失败", "无法保存模板")
                
    def on_load_template_button_clicked(self):
        """加载模板按钮点击事件"""
        # 让用户选择模板
        template_data = self.template_manager.load_template()
        
        if template_data:
            # 应用模板设置
            self._apply_template_settings(template_data)
            QMessageBox.information(self, "加载成功", "模板已加载")
            
    def on_delete_template_button_clicked(self):
        """删除模板按钮点击事件"""
        # 获取选中的模板
        current_item = self.template_list_widget.currentItem()
        if current_item:
            template_name = current_item.text()
            # 删除模板
            if self.template_manager.delete_template(template_name):
                # 更新模板列表
                self.update_template_list()
                QMessageBox.information(self, "删除成功", f"模板 '{template_name}' 已删除")
            else:
                QMessageBox.warning(self, "删除失败", "无法删除模板")
        else:
            QMessageBox.warning(self, "警告", "请先选择要删除的模板")
            
    def on_template_item_clicked(self, item):
        """模板列表项点击事件"""
        template_name = item.text()
        # 加载模板
        template_data = self.template_manager.load_template(template_name)
        
        if template_data:
            # 应用模板设置
            self._apply_template_settings(template_data)
            
    def update_template_list(self):
        """更新模板列表"""
        self.template_list_widget.clear()
        # 获取所有模板
        templates = self.template_manager.get_all_templates()
        # 添加到列表
        for template in templates:
            self.template_list_widget.addItem(template)
            
    def _get_color_from_preview(self):
        """从颜色预览标签中获取颜色值"""
        style_sheet = self.color_preview.styleSheet()
        # 从样式表中提取RGB值
        start = style_sheet.find("rgba(") + 5
        end = style_sheet.find(")", start)
        if start > 5 and end > start:
            rgba_values = style_sheet[start:end].split(",")
            if len(rgba_values) >= 3:
                try:
                    r = int(rgba_values[0].strip())
                    g = int(rgba_values[1].strip())
                    b = int(rgba_values[2].strip())
                    return (r, g, b)
                except ValueError:
                    pass
        return (255, 255, 255)  # 默认白色
        
    def _get_selected_position(self):
        """获取选中的位置"""
        for position, button in self.position_buttons.items():
            if button.isChecked():
                return position
        return "center"  # 默认居中
        
    def _apply_template_settings(self, template_data):
        """应用模板设置"""
        # 设置水印文本
        self.watermark_text_edit.setText(template_data.get("text", ""))
        self.watermark.set_text(template_data.get("text", ""))
        
        # 设置字体
        font_name = template_data.get("font_name", "Arial")
        font_size = template_data.get("font_size", 24)
        font_bold = template_data.get("font_bold", False)
        font_italic = template_data.get("font_italic", False)
        
        self.font_name_label.setText(font_name)
        self.font_size_spinbox.setValue(font_size)
        self.bold_checkbox.setChecked(font_bold)
        self.italic_checkbox.setChecked(font_italic)
        self.watermark.set_font(font_name, font_size, font_bold, font_italic)
        
        # 设置颜色和透明度
        color = template_data.get("color", (255, 255, 255))
        opacity = template_data.get("opacity", 50)
        
        self.opacity_slider.setValue(opacity)
        self.opacity_label.setText(f"{opacity}%")
        if isinstance(color, (list, tuple)) and len(color) >= 3:
            r, g, b = color[:3]
            self.color_preview.setStyleSheet(
                f"background-color: rgba({r}, {g}, {b}, {int(opacity * 2.55)}); border: 1px solid #ccc;"
            )
            # 设置水印颜色
            self.watermark.set_color(r, g, b, opacity)
        
        # 设置位置
        position = template_data.get("position", "center")
        if position in self.position_buttons:
            self.position_buttons[position].setChecked(True)
            self.watermark.set_position(position)
        
        # 设置旋转角度
        rotation = template_data.get("rotation", 0)
        self.rotation_slider.setValue(rotation)
        self.rotation_label.setText(f"{rotation}°")
        self.watermark.set_rotation(rotation)
        
        # 更新预览
        self.update_preview()
        
    def load_settings(self):
        """加载上次的设置"""
        # 这里可以实现从配置文件加载设置的逻辑
        # 目前简化处理
        pass
        
    def save_settings(self):
        """保存当前设置"""
        # 这里可以实现保存设置到配置文件的逻辑
        # 目前简化处理
        pass
        
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 保存设置
        self.save_settings()
        event.accept()