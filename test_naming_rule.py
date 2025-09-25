import os
from src.core.file_handler import FileHandler

# 测试get_output_file_path方法的功能
def test_naming_rules():
    file_handler = FileHandler()
    
    # 测试用例
    image_path = "C:/test/image.jpg"
    output_folder = "C:/output"
    prefix = "watermark_"
    suffix = "_edited"
    
    # 测试原始命名规则
    output_path_original = file_handler.get_output_file_path(
        image_path, output_folder, "original", prefix, suffix
    )
    print(f"原始命名规则: {output_path_original}")
    # 应该输出: C:/output/image.jpg
    
    # 测试前缀命名规则
    output_path_prefix = file_handler.get_output_file_path(
        image_path, output_folder, "prefix", prefix, suffix
    )
    print(f"前缀命名规则: {output_path_prefix}")
    # 应该输出: C:/output/watermark_image.jpg
    
    # 测试后缀命名规则
    output_path_suffix = file_handler.get_output_file_path(
        image_path, output_folder, "suffix", prefix, suffix
    )
    print(f"后缀命名规则: {output_path_suffix}")
    # 应该输出: C:/output/image_edited.jpg
    
    # 验证结果
    expected_original = os.path.join(output_folder, "image.jpg")
    expected_prefix = os.path.join(output_folder, "watermark_image.jpg")
    expected_suffix = os.path.join(output_folder, "image_edited.jpg")
    
    assert output_path_original == expected_original, f"原始命名规则失败: 期望 {expected_original}，得到 {output_path_original}"
    assert output_path_prefix == expected_prefix, f"前缀命名规则失败: 期望 {expected_prefix}，得到 {output_path_prefix}"
    assert output_path_suffix == expected_suffix, f"后缀命名规则失败: 期望 {expected_suffix}，得到 {output_path_suffix}"
    
    print("所有命名规则测试通过！")

if __name__ == "__main__":
    test_naming_rules()