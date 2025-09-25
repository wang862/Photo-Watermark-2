// Watermark.cpp - 水印类实现
#include "Watermark.h"

// 构造函数
Watermark::Watermark() 
    : text("Sample Watermark"),
      fontName("Arial"),
      fontSize(24),
      isBold(false),
      isItalic(false),
      color(0, 0, 0, 128), // 默认黑色半透明
      opacity(0.5f),
      positionX(0),
      positionY(0),
      rotationAngle(0.0f) {
}

Watermark::Watermark(const std::string& txt, const std::string& font, int size,
                   bool bold, bool italic, const Color& col, float opac,
                   int posX, int posY, float rotAngle)
    : text(txt),
      fontName(font),
      fontSize(size),
      isBold(bold),
      isItalic(italic),
      color(col),
      opacity(opac),
      positionX(posX),
      positionY(posY),
      rotationAngle(rotAngle) {
}

// 设置和获取水印文本
void Watermark::setText(const std::string& txt) {
    text = txt;
}

std::string Watermark::getText() const {
    return text;
}

// 设置和获取字体属性
void Watermark::setFontName(const std::string& font) {
    fontName = font;
}

std::string Watermark::getFontName() const {
    return fontName;
}

void Watermark::setFontSize(int size) {
    if (size > 0) {
        fontSize = size;
    }
}

int Watermark::getFontSize() const {
    return fontSize;
}

void Watermark::setBold(bool bold) {
    isBold = bold;
}

bool Watermark::getBold() const {
    return isBold;
}

void Watermark::setItalic(bool italic) {
    isItalic = italic;
}

bool Watermark::getItalic() const {
    return isItalic;
}

// 设置和获取颜色
void Watermark::setColor(const Color& col) {
    color = col;
}

Color Watermark::getColor() const {
    return color;
}

// 设置和获取透明度 (0-1.0)
void Watermark::setOpacity(float opac) {
    if (opac < 0.0f) opac = 0.0f;
    if (opac > 1.0f) opac = 1.0f;
    opacity = opac;
    // 同时更新颜色的alpha通道
    color.a = static_cast<int>(opac * 255);
}

float Watermark::getOpacity() const {
    return opacity;
}

// 设置和获取透明度百分比 (0-100%)
void Watermark::setOpacityPercentage(int percent) {
    if (percent < 0) percent = 0;
    if (percent > 100) percent = 100;
    opacity = static_cast<float>(percent) / 100.0f;
    // 同时更新颜色的alpha通道
    color.a = static_cast<int>(opacity * 255);
}

int Watermark::getOpacityPercentage() const {
    return static_cast<int>(opacity * 100);
}

// 设置和获取位置
void Watermark::setPosition(int x, int y) {
    positionX = x;
    positionY = y;
}

int Watermark::getPositionX() const {
    return positionX;
}

int Watermark::getPositionY() const {
    return positionY;
}

// 设置和获取旋转角度
void Watermark::setRotationAngle(float angle) {
    rotationAngle = angle;
}

float Watermark::getRotationAngle() const {
    return rotationAngle;
}

// 重置水印设置为默认值
void Watermark::resetToDefault() {
    text = "Sample Watermark";
    fontName = "Arial";
    fontSize = 24;
    isBold = false;
    isItalic = false;
    color = Color(0, 0, 0, 128); // 默认黑色半透明
    opacity = 0.5f;
    positionX = 0;
    positionY = 0;
    rotationAngle = 0.0f;
}