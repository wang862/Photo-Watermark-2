# -*- coding: utf-8 -*-
"""
测试模板保存和加载功能
"""
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import sys

# 导入应用程序的模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.template_manager import TemplateManager

class TestTemplateApp(QWidget):
    def __init__(self):
        super().__init__()
        self.template_manager = TemplateManager(self)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('测试模板功能')
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # 测试模板保存
        self.template_name_edit = QLineEdit()
        self.template_name_edit.setPlaceholderText('输入模板名称')
        layout.addWidget(self.template_name_edit)
        
        self.save_button = QPushButton('保存测试模板')
        self.save_button.clicked.connect(self.on_save_test_template)
        layout.addWidget(self.save_button)
        
        # 测试模板加载
        self.load_button = QPushButton('加载测试模板')
        self.load_button.clicked.connect(self.on_load_test_template)
        layout.addWidget(self.load_button)
        
        # 显示结果
        self.result_label = QLabel('测试结果将显示在这里')
        self.result_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(self.result_label)
        
        # 显示模板文件夹路径
        self.folder_label = QLabel(f'模板文件夹: {self.template_manager.get_template_folder()}')
        layout.addWidget(self.folder_label)
        
        self.setLayout(layout)
    
    def on_save_test_template(self):
        template_name = self.template_name_edit.text().strip()
        if not template_name:
            QMessageBox.warning(self, '警告', '请输入模板名称')
            return
        
        # 创建测试模板数据
        template_data = {
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
        success = self.template_manager.save_template(template_name, template_data)
        if success:
            self.result_label.setText(f'模板 "{template_name}" 保存成功！\n\n保存的模板数据：\n{json.dumps(template_data, ensure_ascii=False, indent=2)}')
            QMessageBox.information(self, '成功', f'模板 "{template_name}" 保存成功')
        else:
            self.result_label.setText(f'模板 "{template_name}" 保存失败！')
            QMessageBox.warning(self, '失败', '模板保存失败')
    
    def on_load_test_template(self):
        # 加载模板
        template_data = self.template_manager.load_template()
        
        if template_data:
            self.result_label.setText(f'模板加载成功！\n\n加载的模板数据：\n{json.dumps(template_data, ensure_ascii=False, indent=2)}')
            
            # 检查颜色值是否正确
            color = template_data.get('color', (255, 255, 255))
            if color != (255, 255, 255):
                color_status = f'颜色值正确: {color}'
            else:
                color_status = f'颜色值错误: {color} (应该不是白色)'
            
            self.result_label.setText(f'{self.result_label.text()}\n\n{color_status}')
            QMessageBox.information(self, '成功', '模板加载成功')
        else:
            self.result_label.setText('模板加载失败！')
            QMessageBox.warning(self, '失败', '模板加载失败')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestTemplateApp()
    window.show()
    sys.exit(app.exec_())