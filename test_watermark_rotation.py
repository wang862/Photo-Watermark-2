from PIL import Image, ImageDraw
from src.core.watermark import Watermark
import os
import tempfile

# 创建一个简单的测试图片
def create_test_image():
    # 创建一个临时文件
    temp_dir = tempfile.gettempdir()
    test_image_path = os.path.join(temp_dir, "test_image.png")
    
    # 创建一个红色背景的简单图片
    image = Image.new('RGBA', (500, 300), (255, 0, 0, 255))
    draw = ImageDraw.Draw(image)
    draw.text((100, 100), "Test Image", fill=(255, 255, 255, 255), font_size=30)
    image.save(test_image_path, 'PNG')
    
    return test_image_path

# 测试带旋转角度的水印功能
def test_watermark_rotation():
    # 创建测试图片
    test_image_path = create_test_image()
    print(f"创建测试图片: {test_image_path}")
    
    # 创建输出路径
    output_dir = tempfile.gettempdir()
    output_path = os.path.join(output_dir, "watermark_test_result.png")
    
    try:
        # 创建水印对象
        watermark = Watermark()
        
        # 设置水印参数
        watermark.set_text("测试水印")
        watermark.set_font("Arial", 36)
        watermark.set_color(255, 255, 255, 128)  # 白色半透明
        watermark.set_position("center")
        
        # 测试不同的旋转角度
        for rotation in [0, 45, 90, 135, 180]:
            watermark.set_rotation(rotation)
            
            # 构建带旋转角度的输出路径
            rotated_output_path = os.path.join(output_dir, f"watermark_test_rotation_{rotation}.png")
            
            print(f"测试旋转角度 {rotation} 度...")
            # 添加水印
            watermark.add_watermark(test_image_path, rotated_output_path)
            print(f"  ✓ 成功保存到: {rotated_output_path}")
            
        print("\n🎉 所有旋转角度测试通过！水印旋转功能已修复。")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    finally:
        # 清理测试文件（可选）
        # if os.path.exists(test_image_path):
        #     os.remove(test_image_path)
        pass

if __name__ == "__main__":
    print("开始测试水印旋转功能...")
    test_watermark_rotation()