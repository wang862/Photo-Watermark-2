#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Photo-Watermark-2 - 图片水印工具
水印处理模块
"""

from PIL import Image, ImageDraw, ImageFont
import os


class Watermark:
    """水印处理类，负责添加文本水印到图片上"""
    
    def __init__(self):
        """初始化水印处理器"""
        self.text = ""
        # 使用支持中文的字体作为默认字体
        self.font_name = "SimHei"  # 黑体，Windows系统默认支持中文
        self.font_size = 24
        self.font_bold = False
        self.font_italic = False
        self.color = (255, 255, 255, 128)  # 默认白色半透明
        self.opacity = 50  # 0-100%
        self.position = "center"  # 预设位置或坐标(x, y)
        self.rotation = 0  # 旋转角度
        # 支持中文的备选字体列表
        self.chinese_fonts = ["SimHei", "Microsoft YaHei", "Arial Unicode MS", "WenQuanYi Micro Hei"]
        
    def set_text(self, text):
        """设置水印文本
        
        Args:
            text: 水印文本内容
        """
        self.text = text
        
    def set_font(self, font_name, font_size, bold=False, italic=False):
        """设置水印字体
        
        Args:
            font_name: 字体名称
            font_size: 字体大小
            bold: 是否粗体
            italic: 是否斜体
        """
        self.font_name = font_name
        self.font_size = font_size
        self.font_bold = bold
        self.font_italic = italic
        
    def set_color(self, r, g, b, opacity=50):
        """设置水印颜色和透明度
        
        Args:
            r: 红色通道值(0-255)
            g: 绿色通道值(0-255)
            b: 蓝色通道值(0-255)
            opacity: 透明度(0-100%)
        """
        self.color = (r, g, b, int(opacity * 2.55))
        self.opacity = opacity
        
    def set_position(self, position):
        """设置水印位置
        
        Args:
            position: 预设位置字符串('top_left', 'top_center', 'top_right', 
                      'middle_left', 'center', 'middle_right', 
                      'bottom_left', 'bottom_center', 'bottom_right')
                      或坐标元组(x, y)
        """
        self.position = position
        
    def set_rotation(self, angle):
        """设置水印旋转角度
        
        Args:
            angle: 旋转角度(度)
        """
        self.rotation = angle
        
    def add_watermark(self, image_path, output_path=None):
        """添加水印到图片
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径，如果为None则返回处理后的Image对象
            
        Returns:
            处理后的Image对象或None(如果指定了output_path)
        """
        if not self.text:
            raise ValueError("水印文本不能为空")
            
        # 打开图片
        try:
            with Image.open(image_path) as img:
                # 确保图片有Alpha通道
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # 创建一个可以在其上绘制的新图像
                watermark_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(watermark_img)
                
                # 加载字体
                font = None
                
                # 1. 首先尝试用户指定的字体
                try:
                    font = ImageFont.truetype(self.font_name, self.font_size)
                    # 测试字体是否支持中文
                    try:
                        # 创建一个临时的draw对象来测试字体
                        test_img = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                        test_draw = ImageDraw.Draw(test_img)
                        test_draw.text((0, 0), "测试", font=font)
                    except Exception:
                        print(f"警告: 指定的字体 '{self.font_name}' 可能不支持中文")
                except IOError:
                    # 字体加载失败，尝试备选中文字体
                    for fallback_font in self.chinese_fonts:
                        try:
                            font = ImageFont.truetype(fallback_font, self.font_size)
                            break
                        except IOError:
                            continue
                    
                    # 如果所有备选字体都失败，尝试直接指定一些常见的中文字体文件路径
                    # Windows系统常见中文字体路径
                    windows_font_paths = [
                        "C:/Windows/Fonts/simhei.ttf",  # 黑体
                        "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
                        "C:/Windows/Fonts/simsun.ttc",  # 宋体
                        "C:/Windows/Fonts/simkai.ttf"   # 楷体
                    ]
                    
                    if font is None:
                        for font_path in windows_font_paths:
                            if os.path.exists(font_path):
                                try:
                                    font = ImageFont.truetype(font_path, self.font_size)
                                    break
                                except IOError:
                                    continue
                    
                    # 如果所有尝试都失败，使用系统默认字体并提示
                    if font is None:
                        font = ImageFont.load_default()
                        print(f"警告: 无法加载指定字体 '{self.font_name}' 和所有备选中文字体，使用系统默认字体")
                
                # 获取文本尺寸
                try:
                    # 尝试使用新的textbbox方法(Pillow 9.0+)
                    text_bbox = draw.textbbox((0, 0), self.text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                except AttributeError:
                    try:
                        # 尝试使用textlength方法
                        text_width = draw.textlength(self.text, font=font)
                        text_height = font.size
                    except AttributeError:
                        # 回退到旧的textsize方法
                        text_width, text_height = draw.textsize(self.text, font=font)
                
                # 计算水印位置
                if isinstance(self.position, tuple) and len(self.position) == 2:
                    # 手动指定的坐标
                    x, y = self.position
                else:
                    # 预设位置
                    img_width, img_height = img.size
                    if self.position == "top_left":
                        x, y = 10, 10
                    elif self.position == "top_center":
                        x, y = (img_width - text_width) // 2, 10
                    elif self.position == "top_right":
                        x, y = img_width - text_width - 10, 10
                    elif self.position == "middle_left":
                        x, y = 10, (img_height - text_height) // 2
                    elif self.position == "center":
                        x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
                    elif self.position == "middle_right":
                        x, y = img_width - text_width - 10, (img_height - text_height) // 2
                    elif self.position == "bottom_left":
                        x, y = 10, img_height - text_height - 10
                    elif self.position == "bottom_center":
                        x, y = (img_width - text_width) // 2, img_height - text_height - 10
                    elif self.position == "bottom_right":
                        x, y = img_width - text_width - 10, img_height - text_height - 10
                    else:
                        # 默认居中
                        x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
                
                # 绘制文本
                draw.text((x, y), self.text, font=font, fill=self.color)
                
                # 如果需要旋转
                if self.rotation != 0:
                    # 优化的旋转方法，只旋转水印文字而不改变原图大小
                    # 创建一个与原图大小相同的透明水印图像
                    rotated_watermark = Image.new('RGBA', img.size, (255, 255, 255, 0))
                    
                    # 创建一个临时图像来绘制和旋转文本
                    # 计算需要的临时图像大小，确保足够容纳旋转后的文本
                    import math
                    max_dim = max(text_width, text_height) * 2
                    temp_img = Image.new('RGBA', (max_dim, max_dim), (255, 255, 255, 0))
                    temp_draw = ImageDraw.Draw(temp_img)
                    
                    # 在临时图像中心绘制文本
                    temp_center = max_dim // 2
                    temp_draw.text(
                        (temp_center - text_width // 2, temp_center - text_height // 2),
                        self.text, font=font, fill=self.color
                    )
                    
                    # 旋转临时图像
                    rotated_temp = temp_img.rotate(self.rotation, expand=1)
                    
                    # 计算在原图上放置旋转后水印的位置
                    rot_width, rot_height = rotated_temp.size
                    
                    # 根据用户选择的位置计算粘贴坐标
                    if isinstance(self.position, tuple) and len(self.position) == 2:
                        # 手动指定的坐标
                        paste_x, paste_y = self.position
                    else:
                        # 预设位置
                        img_width, img_height = img.size
                        if self.position == "top_left":
                            paste_x, paste_y = 0, 0
                        elif self.position == "top_center":
                            paste_x, paste_y = (img_width - rot_width) // 2, 0
                        elif self.position == "top_right":
                            paste_x, paste_y = img_width - rot_width, 0
                        elif self.position == "middle_left":
                            paste_x, paste_y = 0, (img_height - rot_height) // 2
                        elif self.position == "center":
                            paste_x, paste_y = (img_width - rot_width) // 2, (img_height - rot_height) // 2
                        elif self.position == "middle_right":
                            paste_x, paste_y = img_width - rot_width, (img_height - rot_height) // 2
                        elif self.position == "bottom_left":
                            paste_x, paste_y = 0, img_height - rot_height
                        elif self.position == "bottom_center":
                            paste_x, paste_y = (img_width - rot_width) // 2, img_height - rot_height
                        elif self.position == "bottom_right":
                            paste_x, paste_y = img_width - rot_width, img_height - rot_height
                        else:
                            # 默认居中
                            paste_x, paste_y = (img_width - rot_width) // 2, (img_height - rot_height) // 2
                    
                    # 将旋转后的水印粘贴到原始大小的水印图像上
                    rotated_watermark.paste(rotated_temp, (paste_x, paste_y), rotated_temp)
                    
                    # 直接在原图上合成水印
                    result = Image.alpha_composite(img, rotated_watermark)
                else:
                    # 不需要旋转，直接合成
                    result = Image.alpha_composite(img, watermark_img)
                
                # 如果指定了输出路径，保存图片
                if output_path:
                    # 根据文件扩展名选择保存格式
                    ext = os.path.splitext(output_path)[1].lower()
                    if ext in ['.jpg', '.jpeg']:
                        # JPEG不支持透明通道，转换为RGB
                        result = result.convert('RGB')
                        result.save(output_path, 'JPEG', quality=95)
                    elif ext == '.png':
                        result.save(output_path, 'PNG')
                    else:
                        # 默认保存为PNG
                        result.save(output_path, 'PNG')
                    return None
                else:
                    return result
        except Exception as e:
            raise Exception(f"添加水印时发生错误: {str(e)}")
            
    def save_template(self, template_name, template_path):
        """保存水印模板
        
        Args:
            template_name: 模板名称
            template_path: 模板保存路径
        """
        import json
        
        template_data = {
            "name": template_name,
            "text": self.text,
            "font_name": self.font_name,
            "font_size": self.font_size,
            "font_bold": self.font_bold,
            "font_italic": self.font_italic,
            "color": self.color,
            "opacity": self.opacity,
            "position": self.position,
            "rotation": self.rotation
        }
        
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template_data, f, ensure_ascii=False, indent=4)
            
    def load_template(self, template_path):
        """加载水印模板
        
        Args:
            template_path: 模板文件路径
        """
        import json
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
                
            self.text = template_data.get("text", "")
            self.font_name = template_data.get("font_name", "Arial")
            self.font_size = template_data.get("font_size", 24)
            self.font_bold = template_data.get("font_bold", False)
            self.font_italic = template_data.get("font_italic", False)
            self.color = tuple(template_data.get("color", (255, 255, 255, 128)))
            self.opacity = template_data.get("opacity", 50)
            self.position = template_data.get("position", "center")
            self.rotation = template_data.get("rotation", 0)
            
        except Exception as e:
            raise Exception(f"加载模板时发生错误: {str(e)}")