#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
文件处理器模块测试
"""

import unittest
import os
import tempfile
from PIL import Image

from core.file_handler import FileHandler


class TestFileHandler(unittest.TestCase):
    """文件处理器模块测试类"""
    
    def setUp(self):
        """测试前的设置"""
        # 创建FileHandler实例
        # 由于FileHandler需要一个父窗口，但我们在测试中不需要实际的GUI
        # 所以我们创建一个简单的模拟对象作为父窗口
        class MockParent:
            def showMessageBox(self, *args):
                pass
        
        self.parent = MockParent()
        self.file_handler = FileHandler(self.parent)
        
        # 创建临时测试目录
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # 创建测试图片
        self._create_test_images()
        
    def tearDown(self):
        """测试后的清理"""
        # 关闭临时目录，自动删除所有临时文件
        self.temp_dir.cleanup()
        
    def _create_test_images(self):
        """创建测试用的图片文件"""
        # 创建不同格式的测试图片
        formats = ["png", "jpg", "bmp"]
        
        self.test_image_paths = []
        for i, ext in enumerate(formats):
            image_path = os.path.join(self.temp_dir.name, f"test_image_{i}.{ext}")
            
            # 创建一个100x100的白色图片
            image = Image.new('RGB', (100, 100), color='white')
            
            # 保存图片
            image.save(image_path)
            
            self.test_image_paths.append(image_path)
            
        # 创建子目录并添加一些图片
        self.sub_dir = os.path.join(self.temp_dir.name, "subdir")
        os.makedirs(self.sub_dir)
        
        self.subdir_image_paths = []
        for i, ext in enumerate(formats):
            image_path = os.path.join(self.sub_dir, f"sub_test_image_{i}.{ext}")
            
            # 创建一个100x100的白色图片
            image = Image.new('RGB', (100, 100), color='white')
            
            # 保存图片
            image.save(image_path)
            
            self.subdir_image_paths.append(image_path)
            
    def test_select_images(self):
        """测试选择图片文件
        注意：这个测试需要模拟QFileDialog的行为，实际测试中可能需要使用测试框架如pytest-qt
        """
        # 在实际的自动化测试中，我们需要模拟QFileDialog的返回值
        # 这里我们只是验证方法是否存在和基本的行为
        try:
            # 由于我们不能在非GUI环境中真正打开文件对话框
            # 我们只是检查方法是否存在而不实际调用它
            self.assertTrue(hasattr(self.file_handler, 'select_images'))
        except Exception as e:
            self.fail(f"select_images方法引发了异常: {str(e)}")
            
    def test_get_files_in_folder(self):
        """测试获取文件夹中的文件"""
        # 获取主目录中的文件
        files = self.file_handler.get_files_in_folder(self.temp_dir.name)
        
        # 检查是否获取了所有的测试图片
        for image_path in self.test_image_paths:
            self.assertIn(image_path, files)
        
        # 检查是否没有包含子目录中的文件（默认不递归）
        for image_path in self.subdir_image_paths:
            self.assertNotIn(image_path, files)
            
        # 测试递归获取文件
        files_recursive = self.file_handler.get_files_in_folder(self.temp_dir.name, recursive=True)
        
        # 检查是否获取了所有的测试图片，包括子目录中的
        for image_path in self.test_image_paths + self.subdir_image_paths:
            self.assertIn(image_path, files_recursive)
            
    def test_select_output_folder(self):
        """测试选择输出文件夹
        注意：这个测试需要模拟QFileDialog的行为，实际测试中可能需要使用测试框架如pytest-qt
        """
        # 在实际的自动化测试中，我们需要模拟QFileDialog的返回值
        # 这里我们只是验证方法是否存在和基本的行为
        try:
            # 由于我们不能在非GUI环境中真正打开文件对话框
            # 我们只是检查方法是否存在而不实际调用它
            self.assertTrue(hasattr(self.file_handler, 'select_output_folder'))
        except Exception as e:
            self.fail(f"select_output_folder方法引发了异常: {str(e)}")
            
    def test_create_folder_if_not_exists(self):
        """测试创建文件夹（如果不存在）"""
        # 定义新文件夹路径
        new_folder = os.path.join(self.temp_dir.name, "new_folder")
        
        # 确保文件夹不存在
        self.assertFalse(os.path.exists(new_folder))
        
        # 创建文件夹
        result = self.file_handler.create_folder_if_not_exists(new_folder)
        
        # 检查是否创建成功
        self.assertTrue(result)
        self.assertTrue(os.path.exists(new_folder))
        self.assertTrue(os.path.isdir(new_folder))
        
        # 测试创建已存在的文件夹
        result = self.file_handler.create_folder_if_not_exists(new_folder)
        
        # 应该返回True，表示操作成功（文件夹已存在）
        self.assertTrue(result)
        
    def test_get_file_name_without_ext(self):
        """测试获取不带扩展名的文件名"""
        # 测试不同格式的文件
        test_files = [
            ("test_image.png", "test_image"),
            ("path/to/file.jpg", "file"),
            ("file_with.many.dots.txt", "file_with.many.dots"),
            ("file_without_ext", "file_without_ext"),
        ]
        
        for file_path, expected_name in test_files:
            actual_name = self.file_handler.get_file_name_without_ext(file_path)
            self.assertEqual(actual_name, expected_name)
            
    def test_get_file_extension(self):
        """测试获取文件扩展名"""
        # 测试不同格式的文件
        test_files = [
            ("test_image.png", ".png"),
            ("path/to/file.jpg", ".jpg"),
            ("file_with.many.dots.txt", ".txt"),
            ("file_without_ext", ""),
        ]
        
        for file_path, expected_ext in test_files:
            actual_ext = self.file_handler.get_file_extension(file_path)
            self.assertEqual(actual_ext, expected_ext)
            
    def test_is_safe_to_save(self):
        """测试检查是否安全保存"""
        # 创建一个临时输出文件
        output_file = os.path.join(self.temp_dir.name, "output.png")
        open(output_file, 'w').close()  # 创建空文件
        
        # 测试保存到不同的文件（应该安全）
        self.assertTrue(self.file_handler.is_safe_to_save(self.test_image_paths[0], output_file))
        
        # 测试保存到同一个文件（应该不安全）
        self.assertFalse(self.file_handler.is_safe_to_save(self.test_image_paths[0], self.test_image_paths[0]))
        
        # 测试保存到不存在的输出文件（应该安全）
        non_existent_output = os.path.join(self.temp_dir.name, "non_existent.png")
        self.assertTrue(self.file_handler.is_safe_to_save(self.test_image_paths[0], non_existent_output))
        
    def test_get_unique_filename(self):
        """测试获取唯一的文件名"""
        # 创建一个临时文件
        base_name = "test_file"
        ext = ".png"
        file_path = os.path.join(self.temp_dir.name, f"{base_name}{ext}")
        open(file_path, 'w').close()  # 创建空文件
        
        # 获取唯一文件名（应该添加数字后缀）
        unique_path = self.file_handler.get_unique_filename(self.temp_dir.name, base_name, ext)
        
        # 检查文件名是否唯一
        self.assertNotEqual(unique_path, file_path)
        self.assertTrue(os.path.basename(unique_path).startswith(f"{base_name}_"))
        
        # 检查文件是否不存在
        self.assertFalse(os.path.exists(unique_path))
        

# 运行测试
if __name__ == "__main__":
    unittest.main()