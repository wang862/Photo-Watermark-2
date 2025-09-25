#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""简单的PyQt5测试脚本"""

try:
    import sys
    from PyQt5.QtWidgets import QApplication, QLabel
    print("PyQt5导入成功")
    
    # 尝试创建一个简单的窗口
    app = QApplication(sys.argv)
    label = QLabel("Hello PyQt5!")
    label.show()
    sys.exit(app.exec_())
except ImportError as e:
    print(f"PyQt5导入失败: {e}")
except Exception as e:
    print(f"发生错误: {e}")