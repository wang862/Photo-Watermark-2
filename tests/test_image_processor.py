#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
图像处理器模块测试
"""

import unittest
import os
import tempfile
from PIL import Image

from core.image_processor import ImageProcessor
from utils.common_utils import is_image_file


class TestImageProcessor(unittest.TestCase):
    """图像处理器模块测试类"""
    
    def setUp(self):
        """测试前的设置"""
        # 创建ImageProcessor实例
        self.image_processor = ImageProcessor()
        
        # 创建临时测试目录
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # 创建临时测试图片
        self.test_image_paths = []
        self._create_test_images()
        
    def tearDown(self):
        """测试后的清理"""
        # 关闭临时目录，自动删除所有临时文件
        self.temp_dir.cleanup()
        
    def _create_test_images(self):
        """创建测试用的图片文件"""
        # 创建不同格式的测试图片
        formats = ["png", "jpg", "bmp"]
        
        for i, ext in enumerate(formats):
            image_path = os.path.join(self.temp_dir.name, f"test_image_{i}.{ext}")
            
            # 创建一个200x200的白色图片
            image = Image.new('RGB', (200, 200), color='white')
            
            # 在图片上绘制一些内容，以便区分
            draw = ImageDraw.Draw(image)
            draw.rectangle([(50, 50), (150, 150)], fill=(0, 0, 255))
            
            # 保存图片
            image.save(image_path)
            
            self.test_image_paths.append(image_path)
            
    def test_load_image(self):
        """测试加载单个图片"""
        # 加载一个测试图片
        result = self.image_processor.load_image(self.test_image_paths[0])
        
        # 检查是否加载成功
        self.assertTrue(result)
        
        # 检查已加载的图片数量
        self.assertEqual(len(self.image_processor.get_loaded_images()), 1)
        
        # 检查加载的图片路径是否正确
        self.assertEqual(self.image_processor.get_loaded_images()[0], self.test_image_paths[0])
        
        # 检查当前图片索引是否正确
        self.assertEqual(self.image_processor.current_image_index, 0)
        
    def test_load_multiple_images(self):
        """测试加载多个图片"""
        # 加载所有测试图片
        for image_path in self.test_image_paths:
            result = self.image_processor.load_image(image_path)
            self.assertTrue(result)
        
        # 检查已加载的图片数量
        self.assertEqual(len(self.image_processor.get_loaded_images()), len(self.test_image_paths))
        
        # 检查加载的图片路径是否正确
        for i, image_path in enumerate(self.image_processor.get_loaded_images()):
            self.assertEqual(image_path, self.test_image_paths[i])
        
    def test_load_invalid_image(self):
        """测试加载无效的图片"""
        # 加载不存在的图片
        result = self.image_processor.load_image("invalid_image.png")
        
        # 检查是否加载失败
        self.assertFalse(result)
        
        # 检查已加载的图片数量（应该没有变化）
        self.assertEqual(len(self.image_processor.get_loaded_images()), 0)
        
    def test_load_folder(self):
        """测试加载文件夹中的图片"""
        # 加载临时目录中的图片
        count = self.image_processor.load_folder(self.temp_dir.name)
        
        # 检查加载的图片数量
        self.assertEqual(count, len(self.test_image_paths))
        
        # 检查已加载的图片路径是否包含所有测试图片
        loaded_images = self.image_processor.get_loaded_images()
        for image_path in self.test_image_paths:
            self.assertIn(image_path, loaded_images)
        
    def test_get_current_image(self):
        """测试获取当前图片"""
        # 先加载图片
        self.image_processor.load_image(self.test_image_paths[0])
        
        # 获取当前图片
        current_image = self.image_processor.get_current_image()
        
        # 检查是否返回了PIL.Image对象
        self.assertIsInstance(current_image, Image.Image)
        
        # 检查图片尺寸是否正确
        self.assertEqual(current_image.size, (200, 200))
        
    def test_set_current_image(self):
        """测试设置当前图片"""
        # 加载多个图片
        for image_path in self.test_image_paths:
            self.image_processor.load_image(image_path)
        
        # 设置当前图片为第二个
        new_index = 1
        self.image_processor.set_current_image(new_index)
        
        # 检查当前图片索引是否正确
        self.assertEqual(self.image_processor.current_image_index, new_index)
        
        # 设置无效的索引
        invalid_index = 100
        with self.assertRaises(IndexError):
            self.image_processor.set_current_image(invalid_index)
        
    def test_remove_image(self):
        """测试移除图片"""
        # 加载多个图片
        for image_path in self.test_image_paths:
            self.image_processor.load_image(image_path)
        
        # 获取初始数量
        initial_count = len(self.image_processor.get_loaded_images())
        
        # 移除第一个图片
        remove_index = 0
        self.image_processor.remove_image(remove_index)
        
        # 检查数量是否减少
        self.assertEqual(len(self.image_processor.get_loaded_images()), initial_count - 1)
        
        # 检查是否移除了正确的图片
        self.assertNotIn(self.test_image_paths[remove_index], self.image_processor.get_loaded_images())
        
        # 移除无效的索引
        invalid_index = 100
        with self.assertRaises(IndexError):
            self.image_processor.remove_image(invalid_index)
        
    def test_clear_images(self):
        """测试清空所有图片"""
        # 加载多个图片
        for image_path in self.test_image_paths:
            self.image_processor.load_image(image_path)
        
        # 清空所有图片
        self.image_processor.clear_images()
        
        # 检查是否清空
        self.assertEqual(len(self.image_processor.get_loaded_images()), 0)
        self.assertEqual(self.image_processor.current_image_index, -1)
        
    def test_get_image_info(self):
        """测试获取图片信息"""
        # 加载图片
        self.image_processor.load_image(self.test_image_paths[0])
        
        # 获取图片信息
        info = self.image_processor.get_image_info(0)
        
        # 检查信息是否正确
        self.assertIsNotNone(info)
        self.assertIn("filename", info)
        self.assertIn("path", info)
        self.assertIn("size", info)
        self.assertIn("dimensions", info)
        
        # 检查文件名是否正确
        self.assertEqual(info["filename"], os.path.basename(self.test_image_paths[0]))
        
        # 检查路径是否正确
        self.assertEqual(info["path"], self.test_image_paths[0])
        
        # 检查尺寸是否正确
        self.assertEqual(info["dimensions"], (200, 200))
        
        # 获取无效索引的信息
        with self.assertRaises(IndexError):
            self.image_processor.get_image_info(100)
        
    def test_create_thumbnail(self):
        """测试创建缩略图"""
        # 定义缩略图尺寸
        thumbnail_size = (100, 100)
        
        # 创建缩略图
        thumbnail = self.image_processor.create_thumbnail(self.test_image_paths[0], thumbnail_size[0], thumbnail_size[1])
        
        # 检查是否返回了PIL.Image对象
        self.assertIsInstance(thumbnail, Image.Image)
        
        # 检查缩略图尺寸是否正确
        self.assertEqual(thumbnail.size, thumbnail_size)
        
        # 创建无效图片的缩略图
        invalid_thumbnail = self.image_processor.create_thumbnail("invalid_image.png", 100, 100)
        self.assertIsNone(invalid_thumbnail)
        
    def test_save_image(self):
        """测试保存图片"""
        # 加载图片
        self.image_processor.load_image(self.test_image_paths[0])
        
        # 定义保存路径
        save_path = os.path.join(self.temp_dir.name, "saved_image.png")
        
        # 保存图片
        result = self.image_processor.save_image(0, save_path)
        
        # 检查是否保存成功
        self.assertTrue(result)
        
        # 检查文件是否存在
        self.assertTrue(os.path.exists(save_path))
        
        # 检查是否为图片文件
        self.assertTrue(is_image_file(save_path))
        
        # 保存无效索引的图片
        with self.assertRaises(IndexError):
            self.image_processor.save_image(100, save_path)
        
    def test_get_loaded_images(self):
        """测试获取已加载的图片列表"""
        # 初始状态应该为空列表
        self.assertEqual(len(self.image_processor.get_loaded_images()), 0)
        
        # 加载图片后检查
        self.image_processor.load_image(self.test_image_paths[0])
        self.assertEqual(len(self.image_processor.get_loaded_images()), 1)
        self.assertEqual(self.image_processor.get_loaded_images()[0], self.test_image_paths[0])
        

# 导入必要的模块（之前的代码中忘记导入ImageDraw）
from PIL import ImageDraw

# 运行测试
if __name__ == "__main__":
    unittest.main()