#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试水印旋转功能修复
确保只旋转水印文字而不改变图片大小
"""

import os
import tempfile
from PIL import Image
from src.core.watermark import Watermark


def create_test_image(width=800, height=600, color=(200, 200, 200)):
    """创建一个简单的测试图片"""
    image = Image.new('RGB', (width, height), color)
    temp_dir = tempfile.gettempdir()
    image_path = os.path.join(temp_dir, "test_image.png")
    image.save(image_path)
    return image_path


def test_watermark_rotation_without_resize():
    """测试水印旋转功能，确保图片大小不变"""
    print("开始测试水印旋转功能（不改变图片大小）...")
    
    # 创建测试图片
    test_image_path = create_test_image(800, 600)
    print(f"创建测试图片: {test_image_path}")
    
    # 获取原图大小
    with Image.open(test_image_path) as img:
        original_width, original_height = img.size
        print(f"原图大小: {original_width}x{original_height}")
    
    # 创建输出路径
    output_dir = tempfile.gettempdir()
    
    try:
        # 创建水印对象
        watermark = Watermark()
        
        # 设置水印参数
        watermark.set_text("测试水印")
        watermark.set_font("SimHei", 48)
        watermark.set_color(255, 0, 0, 128)  # 红色半透明
        watermark.set_position("center")
        
        # 测试不同的旋转角度
        for rotation in [0, 45, 90, 135, 180]:
            watermark.set_rotation(rotation)
            
            # 构建带旋转角度的输出路径
            rotated_output_path = os.path.join(output_dir, f"watermark_test_rotation_{rotation}.png")
            
            print(f"测试旋转角度 {rotation} 度...")
            # 添加水印
            watermark.add_watermark(test_image_path, rotated_output_path)
            
            # 检查输出图片大小是否与原图相同
            with Image.open(rotated_output_path) as result_img:
                result_width, result_height = result_img.size
                print(f"  输出图片大小: {result_width}x{result_height}")
                
                # 验证图片大小是否保持不变
                if result_width == original_width and result_height == original_height:
                    print(f"  ✓ 成功：图片大小保持不变")
                else:
                    print(f"  ✗ 失败：图片大小发生了变化")
        
        print("\n🎉 所有旋转角度测试完成！")
        print(f"测试结果保存在：{output_dir}")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    finally:
        # 清理测试文件（可选）
        # if os.path.exists(test_image_path):
        #     os.remove(test_image_path)
        pass


if __name__ == "__main__":
    test_watermark_rotation_without_resize()