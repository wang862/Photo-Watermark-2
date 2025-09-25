# -*- coding: utf-8 -*-
"""
命令行版本的模板保存和加载测试脚本
直接在终端中验证模板功能是否正常工作
"""
import os
import json
import sys

# 导入应用程序的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.template_manager import TemplateManager

class CommandLineTemplateTester:
    def __init__(self):
        # 创建一个简单的对象作为parent参数
        self.dummy_parent = type('DummyParent', (), {})()
        self.template_manager = TemplateManager(self.dummy_parent)
        self.test_template_name = "test_template_validation"
        print("=== 模板保存和加载功能测试 ===")
        print(f"模板文件夹路径: {self.template_manager.get_template_folder()}")
    
    def run_test(self):
        print("\n[1/3] 测试模板保存功能...")
        self.test_save_template()
        
        print("\n[2/3] 测试模板列表获取功能...")
        self.test_get_templates()
        
        print("\n[3/3] 测试模板加载功能...")
        self.test_load_template()
        
        print("\n=== 测试完成 ===")
    
    def test_save_template(self):
        # 创建测试模板数据
        self.test_template_data = {
            'text': '测试水印',
            'font_name': 'SimHei',
            'font_size': 36,
            'font_bold': True,
            'font_italic': False,
            'color': (255, 0, 0),  # 红色
            'opacity': 70,
            'position': 'bottom_right',
            'rotation': 15
        }
        
        # 保存模板
        success = self.template_manager.save_template(self.test_template_name, self.test_template_data)
        if success:
            print(f"✓ 成功: 模板 '{self.test_template_name}' 保存成功")
            print(f"  保存的模板数据: {json.dumps(self.test_template_data, ensure_ascii=False)}")
        else:
            print(f"✗ 失败: 模板 '{self.test_template_name}' 保存失败")
            sys.exit(1)
    
    def test_get_templates(self):
        # 获取所有模板
        templates = self.template_manager.get_all_templates()
        print(f"✓ 成功: 获取到 {len(templates)} 个模板")
        print(f"  模板列表: {', '.join(templates)}")
        
        # 检查测试模板是否在列表中
        if self.test_template_name in templates:
            print(f"✓ 成功: 测试模板 '{self.test_template_name}' 存在于模板列表中")
        else:
            print(f"✗ 失败: 测试模板 '{self.test_template_name}' 不在模板列表中")
            sys.exit(1)
    
    def test_load_template(self):
        # 加载模板
        loaded_data = self.template_manager.load_template(self.test_template_name)
        
        if loaded_data:
            print(f"✓ 成功: 模板 '{self.test_template_name}' 加载成功")
            print(f"  加载的模板数据: {json.dumps(loaded_data, ensure_ascii=False)}")
            
            # 验证加载的数据是否与保存的数据一致
            is_match = self._compare_template_data(self.test_template_data, loaded_data)
            if is_match:
                print("✓ 成功: 加载的模板数据与保存的完全一致")
            else:
                print("✗ 失败: 加载的模板数据与保存的不一致")
                sys.exit(1)
        else:
            print(f"✗ 失败: 模板 '{self.test_template_name}' 加载失败")
            sys.exit(1)
    
    def _compare_template_data(self, original, loaded):
        """比较两个模板数据是否一致"""
        if set(original.keys()) != set(loaded.keys()):
            print(f"  差异: 键集合不同 - 原始: {set(original.keys())}, 加载: {set(loaded.keys())}")
            return False
        
        for key, value in original.items():
            if key not in loaded:
                print(f"  差异: 键 '{key}' 在加载的数据中不存在")
                return False
            
            loaded_value = loaded[key]
            # 处理浮点数比较（如果有）
            if isinstance(value, float) and isinstance(loaded_value, float):
                if abs(value - loaded_value) > 0.001:
                    print(f"  差异: 键 '{key}' 值不匹配 - 原始: {value}, 加载: {loaded_value}")
                    return False
            elif value != loaded_value:
                print(f"  差异: 键 '{key}' 值不匹配 - 原始: {value}, 加载: {loaded_value}")
                return False
        
        return True

if __name__ == '__main__':
    tester = CommandLineTemplateTester()
    tester.run_test()