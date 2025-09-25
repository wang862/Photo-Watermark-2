#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
预览窗口组件
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt5.QtCore import Qt, QSize, QPoint


class PreviewWidget(QWidget):
    """图片预览窗口组件"""
    
    def __init__(self, parent=None):
        """初始化预览窗口"""
        super().__init__(parent)
        
        # 设置窗口属性
        self.setMinimumHeight(300)
        self.setStyleSheet("background-color: #f5f5f5;")
        
        # 初始化布局
        self.setup_ui()
        
        # 存储当前显示的图片
        self.current_image = None
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建标题标签
        self.title_label = QLabel("预览窗口")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; margin: 5px;")
        main_layout.addWidget(self.title_label)
        
        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        
        # 创建图片显示区域
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        
        # 将图片标签添加到滚动区域
        self.scroll_area.setWidget(self.image_label)
        
        # 添加滚动区域到主布局
        main_layout.addWidget(self.scroll_area)
        
    def set_image(self, image):
        """设置要显示的图片
        
        Args:
            image: 可以是QPixmap、QImage对象、PIL Image对象或文件路径
        """
        # 存储当前图片
        self.current_image = image
        
        # 转换为QPixmap对象
        pixmap = None
        if isinstance(image, str):  # 文件路径
            pixmap = QPixmap(image)
        elif isinstance(image, QImage):
            pixmap = QPixmap.fromImage(image)
        elif isinstance(image, QPixmap):
            pixmap = image
        else:
            # 尝试处理PIL Image对象
            try:
                # 导入PIL和numpy（用于更可靠的图像转换）
                from PIL import Image
                import numpy as np
                
                # 确保我们正在处理PIL Image对象
                if isinstance(image, Image.Image):
                    print(f"处理PIL Image，模式: {image.mode}, 尺寸: {image.width}x{image.height}")
                    
                    # 使用numpy数组作为中间媒介进行转换
                    try:
                        # 将PIL图像转换为numpy数组
                        img_array = np.array(image)
                        height, width, channels = img_array.shape
                        
                        # 根据图像模式选择正确的QImage格式
                        if image.mode == 'RGBA':
                            # RGBA模式 - 确保是32位格式
                            bytes_per_line = 4 * width
                            qimage = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
                        elif image.mode == 'RGB':
                            # RGB模式 - 确保是24位格式
                            bytes_per_line = 3 * width
                            qimage = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        else:
                            # 其他模式先转换为RGB
                            print(f"转换图像模式 {image.mode} 到 RGB")
                            rgb_image = image.convert('RGB')
                            rgb_array = np.array(rgb_image)
                            bytes_per_line = 3 * width
                            qimage = QImage(rgb_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
                        
                        # 转换为QPixmap
                        pixmap = QPixmap.fromImage(qimage)
                        print("PIL Image到QPixmap转换成功")
                    except Exception as numpy_error:
                        print(f"使用numpy转换失败: {str(numpy_error)}")
                        # 备用方法：使用tobytes直接转换
                        if image.mode == 'RGBA':
                            qimage = QImage(image.tobytes('raw', 'BGRA'), image.width, image.height, QImage.Format_RGBA8888)
                        elif image.mode == 'RGB':
                            qimage = QImage(image.tobytes('raw', 'BGR'), image.width, image.height, QImage.Format_RGB888)
                        else:
                            rgb_image = image.convert('RGB')
                            qimage = QImage(rgb_image.tobytes('raw', 'BGR'), rgb_image.width, rgb_image.height, QImage.Format_RGB888)
                        pixmap = QPixmap.fromImage(qimage)
                else:
                    print(f"未知的图片类型: {type(image)}")
                    pixmap = None
            except Exception as e:
                # 更详细的错误处理
                print(f"PIL Image转换错误: {str(e)}")
                # 最后的备用方法：保存为临时文件然后加载
                try:
                    import tempfile
                    import os
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                        temp_path = temp_file.name
                    image.save(temp_path)
                    pixmap = QPixmap(temp_path)
                    os.unlink(temp_path)  # 删除临时文件
                    print("使用临时文件方法转换成功")
                except Exception as last_resort_error:
                    print(f"所有转换方法均失败: {str(last_resort_error)}")
                    pixmap = None
        
        # 显示图片
        if pixmap and not pixmap.isNull():
            # 缩放图片以适应显示区域，但保持原始比例
            scaled_pixmap = self._scale_image(pixmap)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setMinimumSize(10, 10)  # 确保标签可以缩小
        else:
            # 显示占位符
            self.image_label.setText("请先选择一张图片")
            self.image_label.setPixmap(QPixmap())
            
    def _scale_image(self, pixmap):
        """缩放图片以适应显示区域，但保持原始比例
        
        Args:
            pixmap: 要缩放的QPixmap对象
        
        Returns:
            缩放后的QPixmap对象
        """
        # 获取滚动区域的可用大小
        scroll_area_size = self.scroll_area.viewport().size()
        
        # 设置最大宽度和高度，留出一些边距
        max_width = scroll_area_size.width() - 20
        max_height = scroll_area_size.height() - 20
        
        # 获取原始图片的大小
        original_size = pixmap.size()
        
        # 如果图片尺寸已经小于最大尺寸，直接返回原图
        if original_size.width() <= max_width and original_size.height() <= max_height:
            return pixmap
        
        # 计算缩放比例，保持宽高比
        scale_factor = min(max_width / original_size.width(), max_height / original_size.height())
        
        # 计算新的尺寸
        new_width = int(original_size.width() * scale_factor)
        new_height = int(original_size.height() * scale_factor)
        
        # 缩放图片
        scaled_pixmap = pixmap.scaled(
            new_width, new_height,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        
        return scaled_pixmap
        
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        # 如果有图片，重新缩放显示
        if self.current_image:
            self.set_image(self.current_image)
        
        super().resizeEvent(event)
        
    def update_preview(self):
        """更新预览窗口"""
        # 如果有图片，重新显示
        if self.current_image:
            self.set_image(self.current_image)
            
    def clear(self):
        """清空预览窗口"""
        self.image_label.setText("无预览图片")
        self.image_label.setPixmap(QPixmap())
        self.current_image = None