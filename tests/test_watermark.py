#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
水印模块测试
"""

import unittest
import os
import tempfile
from PIL import Image

from core.watermark import Watermark
from utils.common_utils import is_image_file


class TestWatermark(unittest.TestCase):
    """水印模块测试类"""
    
    def setUp(self):
        """测试前的设置"""
        # 创建Watermark实例
        self.watermark = Watermark()
        
        # 创建临时测试图片
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_image_path = os.path.join(self.temp_dir.name, "test_image.png")
        
        # 创建一个简单的测试图片
        self._create_test_image()
        
        # 创建输出文件路径
        self.output_image_path = os.path.join(self.temp_dir.name, "output_with_watermark.png")
        
    def tearDown(self):
        """测试后的清理"""
        # 关闭临时目录，自动删除所有临时文件
        self.temp_dir.cleanup()
        
    def _create_test_image(self):
        """创建测试用的图片文件"""
        # 创建一个200x200的白色图片
        image = Image.new('RGB', (200, 200), color='white')
        
        # 保存图片
        image.save(self.test_image_path)
        
    def test_set_text(self):
        """测试设置水印文本"""
        text = "测试水印"
        self.watermark.set_text(text)
        
        # 检查文本是否正确设置
        self.assertEqual(self.watermark.text, text)
        
    def test_set_font(self):
        """测试设置字体"""
        font_name = "Arial"
        font_size = 24
        self.watermark.set_font(font_name, font_size)
        
        # 检查字体是否正确设置
        self.assertEqual(self.watermark.font_name, font_name)
        self.assertEqual(self.watermark.font_size, font_size)
        
    def test_set_color(self):
        """测试设置颜色"""
        color = (255, 0, 0)  # 红色
        self.watermark.set_color(color)
        
        # 检查颜色是否正确设置
        self.assertEqual(self.watermark.color, color)
        
    def test_set_opacity(self):
        """测试设置透明度"""
        opacity = 70
        self.watermark.set_opacity(opacity)
        
        # 检查透明度是否正确设置
        self.assertEqual(self.watermark.opacity, opacity)
        self.assertEqual(self.watermark.alpha, int(opacity * 2.55))
        
    def test_set_position(self):
        """测试设置位置"""
        positions = ["top_left", "top_center", "top_right",
                     "middle_left", "center", "middle_right",
                     "bottom_left", "bottom_center", "bottom_right"]
        
        for position in positions:
            self.watermark.set_position(position)
            self.assertEqual(self.watermark.position, position)
        
        # 测试无效位置
        self.watermark.set_position("invalid_position")
        self.assertEqual(self.watermark.position, "center")  # 应该默认为center
        
    def test_set_rotation(self):
        """测试设置旋转角度"""
        rotation = 45
        self.watermark.set_rotation(rotation)
        
        # 检查旋转角度是否正确设置
        self.assertEqual(self.watermark.rotation, rotation)
        
    def test_add_watermark(self):
        """测试添加水印到图片"""
        # 设置水印属性
        self.watermark.set_text("测试水印")
        self.watermark.set_font("Arial", 24)
        self.watermark.set_color((0, 0, 0))  # 黑色
        self.watermark.set_opacity(100)  # 不透明
        self.watermark.set_position("center")
        
        # 添加水印
        result = self.watermark.add_watermark(self.test_image_path, self.output_image_path)
        
        # 检查是否成功
        self.assertTrue(result)
        
        # 检查输出文件是否存在
        self.assertTrue(os.path.exists(self.output_image_path))
        
        # 检查输出文件是否为图片文件
        self.assertTrue(is_image_file(self.output_image_path))
        
    def test_add_watermark_with_invalid_image(self):
        """测试添加水印到无效的图片文件"""
        # 设置水印属性
        self.watermark.set_text("测试水印")
        
        # 添加水印到不存在的文件
        result = self.watermark.add_watermark("invalid_image.png", self.output_image_path)
        
        # 检查是否失败
        self.assertFalse(result)
        
    def test_save_and_load_template(self):
        """测试保存和加载水印模板"""
        # 设置水印属性
        self.watermark.set_text("测试模板")
        self.watermark.set_font("Arial", 36)
        self.watermark.set_color((255, 0, 0))
        self.watermark.set_opacity(50)
        self.watermark.set_position("bottom_right")
        self.watermark.set_rotation(30)
        
        # 保存模板
        template_path = os.path.join(self.temp_dir.name, "test_template.json")
        self.watermark.save_template(template_path)
        
        # 检查模板文件是否存在
        self.assertTrue(os.path.exists(template_path))
        
        # 创建新的Watermark实例
        new_watermark = Watermark()
        
        # 加载模板
        new_watermark.load_template(template_path)
        
        # 检查加载的属性是否正确
        self.assertEqual(new_watermark.text, "测试模板")
        self.assertEqual(new_watermark.font_name, "Arial")
        self.assertEqual(new_watermark.font_size, 36)
        self.assertEqual(new_watermark.color, (255, 0, 0))
        self.assertEqual(new_watermark.opacity, 50)
        self.assertEqual(new_watermark.position, "bottom_right")
        self.assertEqual(new_watermark.rotation, 30)
        
    def test_batch_add_watermark(self):
        """测试批量添加水印"""
        # 创建多个测试图片
        test_images = []
        for i in range(3):
            image_path = os.path.join(self.temp_dir.name, f"test_image_{i}.png")
            image = Image.new('RGB', (200, 200), color='white')
            image.save(image_path)
            test_images.append(image_path)
        
        # 设置水印属性
        self.watermark.set_text("批量水印")
        
        # 批量添加水印
        output_paths = []
        for i, image_path in enumerate(test_images):
            output_path = os.path.join(self.temp_dir.name, f"output_{i}.png")
            output_paths.append(output_path)
            result = self.watermark.add_watermark(image_path, output_path)
            self.assertTrue(result)
        
        # 检查所有输出文件是否存在
        for output_path in output_paths:
            self.assertTrue(os.path.exists(output_path))
            self.assertTrue(is_image_file(output_path))
            
    def test_add_watermark_return_image(self):
        """测试添加水印并返回图片对象"""
        # 设置水印属性
        self.watermark.set_text("返回图片对象")
        
        # 添加水印并获取图片对象
        image_obj = self.watermark.add_watermark(self.test_image_path)
        
        # 检查返回的是否为PIL.Image对象
        self.assertIsInstance(image_obj, Image.Image)
        

# 运行测试
if __name__ == "__main__":
    unittest.main()