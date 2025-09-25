// Watermark.h - 水印类头文件
#ifndef WATERMARK_H
#define WATERMARK_H

#include <string>

// 颜色结构
struct Color {
    int r; // 红色通道 (0-255)
    int g; // 绿色通道 (0-255)
    int b; // 蓝色通道 (0-255)
    int a; //  alpha通道 (0-255)

    Color() : r(0), g(0), b(0), a(255) {}
    Color(int red, int green, int blue, int alpha = 255) 
        : r(red), g(green), b(blue), a(alpha) {}
};

// 水印类 - 表示水印的各种属性
class Watermark {
private:
    std::string text;        // 水印文本内容
    std::string fontName;    // 字体名称
    int fontSize;            // 字体大小
    bool isBold;             // 是否粗体
    bool isItalic;           // 是否斜体
    Color color;             // 水印颜色
    float opacity;           // 透明度 (0.0-1.0)
    int positionX;           // X坐标位置
    int positionY;           // Y坐标位置
    float rotationAngle;     // 旋转角度 (度)

public:
    // 构造函数
    Watermark();
    Watermark(const std::string& txt, const std::string& font, int size,
              bool bold, bool italic, const Color& col, float opac,
              int posX, int posY, float rotAngle);

    // 设置和获取水印文本
    void setText(const std::string& txt);
    std::string getText() const;

    // 设置和获取字体属性
    void setFontName(const std::string& font);
    std::string getFontName() const;
    
    void setFontSize(int size);
    int getFontSize() const;
    
    void setBold(bool bold);
    bool getBold() const;
    
    void setItalic(bool italic);
    bool getItalic() const;

    // 设置和获取颜色
    void setColor(const Color& col);
    Color getColor() const;

    // 设置和获取透明度 (0-100%)
    void setOpacity(float opac); // opac范围: 0.0-1.0
    float getOpacity() const;
    void setOpacityPercentage(int percent); // percent范围: 0-100
    int getOpacityPercentage() const;

    // 设置和获取位置
    void setPosition(int x, int y);
    int getPositionX() const;
    int getPositionY() const;

    // 设置和获取旋转角度
    void setRotationAngle(float angle);
    float getRotationAngle() const;

    // 重置水印设置为默认值
    void resetToDefault();
};

#endif // WATERMARK_H