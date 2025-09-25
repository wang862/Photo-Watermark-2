#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
图像处理器模块
"""

from PIL import Image
import os
import tempfile


class ImageProcessor:
    """图像处理器类，负责图像的加载、预览和保存等操作"""
    
    def __init__(self):
        """初始化图像处理器"""
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp']
        self.loaded_images = []  # 存储已加载的图片路径列表
        self.current_image_index = -1  # 当前选中的图片索引
        self.temp_folder = tempfile.gettempdir()
        
    def is_supported_format(self, file_path):
        """检查文件格式是否受支持
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否支持该格式
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.supported_formats
        
    def load_image(self, file_path):
        """加载单个图片
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            Image: 加载的图像对象
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        if not self.is_supported_format(file_path):
            raise ValueError(f"不支持的文件格式: {file_path}")
            
        try:
            with Image.open(file_path) as img:
                # 确保图片有Alpha通道（如果是PNG格式）
                if file_path.lower().endswith('.png') and img.mode != 'RGBA':
                    img = img.convert('RGBA')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 添加到已加载图片列表
                if file_path not in self.loaded_images:
                    self.loaded_images.append(file_path)
                    self.current_image_index = len(self.loaded_images) - 1
                
                return img.copy()
        except Exception as e:
            raise Exception(f"加载图片时发生错误: {str(e)}")
            
    def load_images(self, file_paths):
        """批量加载图片
        
        Args:
            file_paths: 图片文件路径列表
            
        Returns:
            list: 成功加载的图片路径列表
        """
        success_paths = []
        for file_path in file_paths:
            try:
                self.load_image(file_path)
                success_paths.append(file_path)
            except Exception:
                # 忽略加载失败的文件
                continue
                
        return success_paths
        
    def load_folder(self, folder_path):
        """加载文件夹中的所有图片
        
        Args:
            folder_path: 文件夹路径
            
        Returns:
            list: 成功加载的图片路径列表
        """
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"不是有效的文件夹: {folder_path}")
            
        file_paths = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and self.is_supported_format(file_path):
                file_paths.append(file_path)
                
        return self.load_images(file_paths)
        
    def get_current_image(self):
        """获取当前选中的图片
        
        Returns:
            Image: 当前选中的图像对象，如果没有选中的图片则返回None
        """
        if self.current_image_index >= 0 and self.current_image_index < len(self.loaded_images):
            return self.load_image(self.loaded_images[self.current_image_index])
        return None
        
    def get_image_thumbnail(self, file_path, max_size=(100, 100)):
        """获取图片的缩略图
        
        Args:
            file_path: 图片文件路径
            max_size: 缩略图的最大尺寸
            
        Returns:
            Image: 缩略图对象
        """
        img = self.load_image(file_path)
        # 使用兼容新版本Pillow的重采样方法
        try:
            # 对于Pillow 10+版本，使用Resampling.LANCZOS
            from PIL import Image
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        except (ImportError, AttributeError):
            try:
                # 对于Pillow 9.x版本，使用LANCZOS
                from PIL import Image
                img.thumbnail(max_size, Image.LANCZOS)
            except AttributeError:
                # 回退到较老版本的ANTIALIAS
                from PIL import Image
                img.thumbnail(max_size, Image.ANTIALIAS)
        return img
        
    def save_image(self, img, output_path, quality=95):
        """保存图像到文件
        
        Args:
            img: 图像对象
            output_path: 输出文件路径
            quality: 保存质量（0-100）
        """
        try:
            # 根据文件扩展名选择保存格式
            ext = os.path.splitext(output_path)[1].lower()
            if ext in ['.jpg', '.jpeg']:
                # JPEG不支持透明通道，转换为RGB
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=quality)
            elif ext == '.png':
                img.save(output_path, 'PNG')
            else:
                # 默认保存为PNG
                img.save(output_path, 'PNG')
        except Exception as e:
            raise Exception(f"保存图片时发生错误: {str(e)}")
            
    def get_image_info(self, file_path):
        """获取图片信息
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            dict: 图片信息字典
        """
        img = self.load_image(file_path)
        return {
            'width': img.width,
            'height': img.height,
            'mode': img.mode,
            'format': img.format,
            'size_kb': os.path.getsize(file_path) / 1024
        }
        
    def clear_loaded_images(self):
        """清除已加载的图片列表"""
        self.loaded_images = []
        self.current_image_index = -1
        
    def set_current_image(self, index):
        """设置当前选中的图片
        
        Args:
            index: 图片索引
        """
        if 0 <= index < len(self.loaded_images):
            self.current_image_index = index
            return True
        return False
        
    def get_loaded_images(self):
        """获取已加载的图片列表
        
        Returns:
            list: 已加载的图片路径列表
        """
        return self.loaded_images.copy()
        
    def remove_image(self, index):
        """从已加载的图片列表中移除指定的图片
        
        Args:
            index: 图片索引
            
        Returns:
            bool: 是否移除成功
        """
        if 0 <= index < len(self.loaded_images):
            del self.loaded_images[index]
            # 如果移除的是当前选中的图片，更新当前索引
            if self.current_image_index >= len(self.loaded_images):
                self.current_image_index = len(self.loaded_images) - 1
            elif self.current_image_index > index:
                self.current_image_index -= 1
            return True
        return False