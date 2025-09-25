#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
模板管理器模块测试
"""

import unittest
import os
import tempfile
import json

from core.template_manager import TemplateManager


class TestTemplateManager(unittest.TestCase):
    """模板管理器模块测试类"""
    
    def setUp(self):
        """测试前的设置"""
        # 创建TemplateManager实例
        # 由于TemplateManager需要一个父窗口，但我们在测试中不需要实际的GUI
        # 所以我们创建一个简单的模拟对象作为父窗口
        class MockParent:
            def showMessageBox(self, *args):
                pass
        
        self.parent = MockParent()
        
        # 创建临时目录作为模板存储位置
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # 初始化TemplateManager，使用临时目录作为模板文件夹
        self.template_manager = TemplateManager(self.parent, template_dir=self.temp_dir.name)
        
        # 创建一些测试模板数据
        self.test_templates = [
            {
                "name": "测试模板1",
                "watermark_text": "测试水印1",
                "font_name": "Arial",
                "font_size": 24,
                "font_color": "#000000",
                "opacity": 0.5,
                "position": "center",
                "rotation": 0,
                "spacing": 20
            },
            {
                "name": "测试模板2",
                "watermark_text": "测试水印2",
                "font_name": "Times New Roman",
                "font_size": 36,
                "font_color": "#FF0000",
                "opacity": 0.7,
                "position": "tile",
                "rotation": 45,
                "spacing": 30
            }
        ]
        
    def tearDown(self):
        """测试后的清理"""
        # 关闭临时目录，自动删除所有临时文件
        self.temp_dir.cleanup()
        
    def test_save_template(self):
        """测试保存模板"""
        # 保存第一个测试模板
        template_name = "测试模板1"
        template_data = self.test_templates[0]
        
        # 由于save_template需要父窗口，但我们在测试中使用模拟对象，所以它应该能够正常工作
        self.template_manager.save_template(template_name, template_data)
        
        # 检查模板文件是否已创建
        template_file_path = os.path.join(self.temp_dir.name, f"{template_name}.json")
        self.assertTrue(os.path.exists(template_file_path))
        
        # 读取并验证保存的模板数据
        with open(template_file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
            
        # 比较保存的数据与原始数据
        self.assertEqual(saved_data, template_data)
        
    def test_load_template(self):
        """测试加载模板"""
        # 首先保存一个测试模板
        template_name = "测试模板1"
        template_data = self.test_templates[0]
        
        # 创建模板文件
        template_file_path = os.path.join(self.temp_dir.name, f"{template_name}.json")
        with open(template_file_path, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=2)
        
        # 加载模板
        loaded_data = self.template_manager.load_template(template_name)
        
        # 比较加载的数据与原始数据
        self.assertEqual(loaded_data, template_data)
        
        # 测试加载不存在的模板
        non_existent_data = self.template_manager.load_template("不存在的模板")
        self.assertIsNone(non_existent_data)
        
    def test_delete_template(self):
        """测试删除模板"""
        # 首先创建一个测试模板文件
        template_name = "测试模板1"
        template_file_path = os.path.join(self.temp_dir.name, f"{template_name}.json")
        with open(template_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.test_templates[0], f, ensure_ascii=False, indent=2)
        
        # 确保模板文件存在
        self.assertTrue(os.path.exists(template_file_path))
        
        # 删除模板
        self.template_manager.delete_template(template_name)
        
        # 检查模板文件是否已删除
        self.assertFalse(os.path.exists(template_file_path))
        
        # 测试删除不存在的模板（不应该抛出异常）
        try:
            self.template_manager.delete_template("不存在的模板")
        except Exception as e:
            self.fail(f"删除不存在的模板时引发了异常: {str(e)}")
            
    def test_get_template_list(self):
        """测试获取模板列表"""
        # 首先创建几个测试模板文件
        template_files = []
        for i in range(3):
            template_name = f"测试模板{i}"
            template_file_path = os.path.join(self.temp_dir.name, f"{template_name}.json")
            with open(template_file_path, 'w', encoding='utf-8') as f:
                json.dump({"name": template_name, "test": True}, f, ensure_ascii=False, indent=2)
            template_files.append(template_name)
        
        # 创建一个非JSON文件，应该被忽略
        non_json_file = os.path.join(self.temp_dir.name, "not_a_template.txt")
        with open(non_json_file, 'w', encoding='utf-8') as f:
            f.write("This is not a template file.")
        
        # 获取模板列表
        template_list = self.template_manager.get_template_list()
        
        # 检查模板列表是否包含所有创建的模板
        for template_name in template_files:
            self.assertIn(template_name, template_list)
            
        # 检查非JSON文件是否被忽略
        self.assertNotIn("not_a_template.txt", template_list)
        
    def test_rename_template(self):
        """测试重命名模板"""
        # 首先创建一个测试模板文件
        old_name = "测试模板1"
        new_name = "重命名后的模板"
        
        old_file_path = os.path.join(self.temp_dir.name, f"{old_name}.json")
        new_file_path = os.path.join(self.temp_dir.name, f"{new_name}.json")
        
        with open(old_file_path, 'w', encoding='utf-8') as f:
            json.dump({"name": old_name, "test": True}, f, ensure_ascii=False, indent=2)
        
        # 确保模板文件存在
        self.assertTrue(os.path.exists(old_file_path))
        
        # 重命名模板
        success = self.template_manager.rename_template(old_name, new_name)
        
        # 检查重命名是否成功
        self.assertTrue(success)
        self.assertFalse(os.path.exists(old_file_path))
        self.assertTrue(os.path.exists(new_file_path))
        
        # 检查重命名后的模板文件内容
        with open(new_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 注意：模板重命名后，文件内容中的name字段不会自动更新
            # 这是因为TemplateManager只负责文件重命名，不负责更新文件内容
            self.assertEqual(data["name"], old_name)
            
        # 测试重命名不存在的模板
        success = self.template_manager.rename_template("不存在的模板", "新名称")
        self.assertFalse(success)
        
        # 测试重命名为已存在的模板名称
        with open(old_file_path, 'w', encoding='utf-8') as f:
            json.dump({"name": old_name, "test": True}, f, ensure_ascii=False, indent=2)
        
        success = self.template_manager.rename_template(old_name, new_name)
        self.assertFalse(success)
        self.assertTrue(os.path.exists(old_file_path))
        self.assertTrue(os.path.exists(new_file_path))
        
    def test_import_template(self):
        """测试导入模板"""
        # 由于import_template需要使用QFileDialog选择文件，这在自动化测试中比较复杂
        # 这里我们只测试该方法是否存在
        self.assertTrue(hasattr(self.template_manager, 'import_template'))
        
    def test_export_template(self):
        """测试导出模板"""
        # 由于export_template需要使用QFileDialog选择保存位置，这在自动化测试中比较复杂
        # 这里我们只测试该方法是否存在
        self.assertTrue(hasattr(self.template_manager, 'export_template'))
        
    def test_get_template_folder(self):
        """测试获取模板文件夹路径"""
        # 获取模板文件夹路径
        template_folder = self.template_manager.get_template_folder()
        
        # 检查返回的路径是否正确
        self.assertEqual(template_folder, self.temp_dir.name)
        
    def test_set_template_folder(self):
        """测试设置模板文件夹"""
        # 创建一个新的临时目录
        new_temp_dir = tempfile.TemporaryDirectory()
        
        try:
            # 设置新的模板文件夹
            self.template_manager.set_template_folder(new_temp_dir.name)
            
            # 检查模板文件夹是否已更新
            self.assertEqual(self.template_manager.get_template_folder(), new_temp_dir.name)
            
        finally:
            # 清理临时目录
            new_temp_dir.cleanup()
        

# 运行测试
if __name__ == "__main__":
    unittest.main()