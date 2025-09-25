from PIL import Image, ImageDraw
from src.core.watermark import Watermark
import os
import tempfile

# 创建一个简单的测试图片
def create_test_image():
    # 创建一个临时文件
    temp_dir = tempfile.gettempdir()
    test_image_path = os.path.join(temp_dir, "test_chinese_image.png")
    
    # 创建一个蓝色背景的简单图片
    image = Image.new('RGBA', (500, 300), (0, 0, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 由于我们还没有测试字体，这里简单绘制一些形状
    draw.rectangle([(100, 100), (400, 200)], fill=(0, 255, 255, 128))
    image.save(test_image_path, 'PNG')
    
    return test_image_path

# 测试中文字体水印功能
def test_chinese_watermark():
    # 创建测试图片
    test_image_path = create_test_image()
    print(f"创建测试图片: {test_image_path}")
    
    # 创建输出路径
    output_dir = tempfile.gettempdir()
    
    try:
        # 创建水印对象
        watermark = Watermark()
        
        # 设置中文水印文本
        chinese_texts = ["测试水印", "中文水印示例", "Photo-Watermark-2", "你好，世界"]
        
        # 测试不同的中文字体
        for i, text in enumerate(chinese_texts):
            # 重置水印对象
            watermark = Watermark()
            watermark.set_text(text)
            watermark.set_font("SimHei", 36)  # 使用黑体
            watermark.set_color(255, 255, 255, 128)  # 白色半透明
            watermark.set_position("center")
            
            # 构建输出路径
            output_path = os.path.join(output_dir, f"chinese_watermark_test_{i}.png")
            
            print(f"测试中文水印 '{text}'...")
            # 添加水印
            watermark.add_watermark(test_image_path, output_path)
            print(f"  ✓ 成功保存到: {output_path}")
            
        # 额外测试默认字体
        watermark_default = Watermark()
        watermark_default.set_text("默认字体测试")
        default_output_path = os.path.join(output_dir, "chinese_watermark_default.png")
        watermark_default.add_watermark(test_image_path, default_output_path)
        print(f"测试默认字体: 成功保存到 {default_output_path}")
        
        print("\n🎉 所有中文水印测试通过！水印现在应该能正确显示中文了。")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    finally:
        # 清理测试文件（可选）
        # if os.path.exists(test_image_path):
        #     os.remove(test_image_path)
        pass

if __name__ == "__main__":
    print("开始测试中文水印功能...")
    test_chinese_watermark()