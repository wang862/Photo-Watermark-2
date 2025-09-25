// ImageProcessor.cpp - 图像处理核心类实现
#include "ImageProcessor.h"
#include <windows.h>
#include <gdiplus.h>
#include <string>
#include <vector>
#include <algorithm>
#include <shlwapi.h>

#pragma comment(lib, "gdiplus.lib")
#pragma comment(lib, "shlwapi.lib")

using namespace Gdiplus;

// 初始化GDI+
class GdiplusInitializer {
private:
    ULONG_PTR gdiplusToken;
    GdiplusStartupInput gdiplusStartupInput;

public:
    GdiplusInitializer() {
        GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
    }

    ~GdiplusInitializer() {
        GdiplusShutdown(gdiplusToken);
    }
};

// 全局GDI+初始化对象
static GdiplusInitializer gdiplusInit;

// 构造函数
ImageProcessor::ImageProcessor()
    : hBitmap(NULL),
      hMemDC(NULL),
      width(0),
      height(0),
      hasAlphaChannel(false) {
}

// 析构函数
ImageProcessor::~ImageProcessor() {
    releaseResources();
}

// 加载图片
bool ImageProcessor::loadImage(const std::string& filePath) {
    // 先释放现有资源
    releaseResources();

    this->filePath = filePath;

    // 使用GDI+加载图片
    Gdiplus::Image* image = Gdiplus::Image::FromFile(std::wstring(filePath.begin(), filePath.end()).c_str());
    if (!image || image->GetLastStatus() != Ok) {
        return false;
    }

    width = image->GetWidth();
    height = image->GetHeight();

    // 检查是否有透明通道
    PixelFormat pixelFormat = image->GetPixelFormat();
    hasAlphaChannel = ((pixelFormat == PixelFormat32bppARGB) || 
                       (pixelFormat == PixelFormat32bppPARGB) ||
                       (pixelFormat == PixelFormat64bppARGB) ||
                       (pixelFormat == PixelFormat64bppPARGB));

    // 创建位图和内存DC
    HDC hDC = GetDC(NULL);
    hMemDC = CreateCompatibleDC(hDC);
    hBitmap = CreateCompatibleBitmap(hDC, width, height);
    ReleaseDC(NULL, hDC);

    if (!hBitmap || !hMemDC) {
        releaseResources();
        delete image;
        return false;
    }

    // 将图片绘制到位图上
    SelectObject(hMemDC, hBitmap);
    Graphics graphics(hMemDC);
    graphics.DrawImage(image, 0, 0, width, height);

    delete image;
    return true;
}

// 保存图片
bool ImageProcessor::saveImage(const std::string& filePath, ImageFormat format) {
    if (!isLoaded()) {
        return false;
    }

    // 根据指定的格式保存图片
    switch (format) {
    case ImageFormat::JPEG:
        return saveAsJPEG(filePath);
    case ImageFormat::PNG:
        return saveAsPNG(filePath);
    case ImageFormat::BMP:
        return saveAsBMP(filePath);
    default:
        return false;
    }
}

// 从HBITMAP创建图片
bool ImageProcessor::createFromHBITMAP(HBITMAP bitmap, int w, int h) {
    releaseResources();

    hBitmap = bitmap;
    width = w;
    height = h;

    HDC hDC = GetDC(NULL);
    hMemDC = CreateCompatibleDC(hDC);
    SelectObject(hMemDC, hBitmap);
    ReleaseDC(NULL, hDC);

    return (hMemDC != NULL);
}

// 应用水印
bool ImageProcessor::applyWatermark(const Watermark& watermark) {
    if (!isLoaded()) {
        return false;
    }

    drawTextWatermark(watermark);
    return true;
}

// 批量处理图片
bool ImageProcessor::batchProcessImages(const std::vector<std::string>& inputPaths,
                                       const std::string& outputFolder,
                                       const Watermark& watermark,
                                       ImageFormat outputFormat) {
    bool allSuccess = true;

    for (const auto& inputPath : inputPaths) {
        ImageProcessor processor;
        if (processor.loadImage(inputPath)) {
            processor.applyWatermark(watermark);
            
            // 构建输出文件路径
            std::string fileName = PathFindFileNameA(inputPath.c_str());
            std::string outputPath = outputFolder + "\\" + fileName;
            
            // 根据输出格式更改文件扩展名
            std::string extension;
            switch (outputFormat) {
            case ImageFormat::JPEG:
                extension = ".jpg";
                break;
            case ImageFormat::PNG:
                extension = ".png";
                break;
            case ImageFormat::BMP:
                extension = ".bmp";
                break;
            default:
                extension = ".jpg";
            }
            
            // 替换文件扩展名
            size_t dotPos = outputPath.find_last_of(".");
            if (dotPos != std::string::npos) {
                outputPath = outputPath.substr(0, dotPos) + extension;
            } else {
                outputPath += extension;
            }
            
            if (!processor.saveImage(outputPath, outputFormat)) {
                allSuccess = false;
            }
        } else {
            allSuccess = false;
        }
    }

    return allSuccess;
}

// 获取图片宽度
int ImageProcessor::getWidth() const {
    return width;
}

// 获取图片高度
int ImageProcessor::getHeight() const {
    return height;
}

// 获取位图句柄
HBITMAP ImageProcessor::getHBITMAP() const {
    return hBitmap;
}

// 检查是否有透明通道
bool ImageProcessor::hasAlpha() const {
    return hasAlphaChannel;
}

// 获取文件路径
std::string ImageProcessor::getFilePath() const {
    return filePath;
}

// 获取预览图片
HBITMAP ImageProcessor::getPreview(int previewWidth, int previewHeight) {
    if (!isLoaded()) {
        return NULL;
    }

    // 创建预览位图
    HDC hDC = GetDC(NULL);
    HBITMAP hPreviewBitmap = CreateCompatibleBitmap(hDC, previewWidth, previewHeight);
    HDC hPreviewDC = CreateCompatibleDC(hDC);
    ReleaseDC(NULL, hDC);

    if (!hPreviewBitmap || !hPreviewDC) {
        if (hPreviewBitmap) DeleteObject(hPreviewBitmap);
        if (hPreviewDC) DeleteDC(hPreviewDC);
        return NULL;
    }

    // 计算缩放比例
    float scaleX = static_cast<float>(previewWidth) / width;
    float scaleY = static_cast<float>(previewHeight) / height;
    float scale = std::min(scaleX, scaleY);

    int scaledWidth = static_cast<int>(width * scale);
    int scaledHeight = static_cast<int>(height * scale);
    int offsetX = (previewWidth - scaledWidth) / 2;
    int offsetY = (previewHeight - scaledHeight) / 2;

    // 绘制预览图片
    SelectObject(hPreviewDC, hPreviewBitmap);
    
    // 填充背景色
    RECT rect = {0, 0, previewWidth, previewHeight};
    HBRUSH hBrush = CreateSolidBrush(RGB(240, 240, 240));
    FillRect(hPreviewDC, &rect, hBrush);
    DeleteObject(hBrush);

    // 绘制图片
    BitBlt(hPreviewDC, offsetX, offsetY, scaledWidth, scaledHeight,
           hMemDC, 0, 0, SRCCOPY);

    DeleteDC(hPreviewDC);
    return hPreviewBitmap;
}

// 释放预览位图
void ImageProcessor::releasePreview(HBITMAP hPreviewBitmap) {
    if (hPreviewBitmap) {
        DeleteObject(hPreviewBitmap);
    }
}

// 检查图片是否已加载
bool ImageProcessor::isLoaded() const {
    return (hBitmap != NULL && hMemDC != NULL);
}

// 清除资源
void ImageProcessor::clear() {
    releaseResources();
}

// 从文件扩展名获取图片格式
ImageFormat ImageProcessor::getFormatFromFileExtension(const std::string& filePath) {
    std::string extension = PathFindExtensionA(filePath.c_str());
    std::transform(extension.begin(), extension.end(), extension.begin(), ::tolower);

    if (extension == ".jpg" || extension == ".jpeg") {
        return ImageFormat::JPEG;
    } else if (extension == ".png") {
        return ImageFormat::PNG;
    } else if (extension == ".bmp") {
        return ImageFormat::BMP;
    } else {
        return ImageFormat::UNKNOWN;
    }
}

// 保存为JPEG格式
bool ImageProcessor::saveAsJPEG(const std::string& filePath) {
    if (!isLoaded()) {
        return false;
    }

    // 使用GDI+保存图片
    Bitmap bitmap(hBitmap, NULL);
    CLSID clsidJpeg;
    GetEncoderClsid(L"image/jpeg", &clsidJpeg);
    return bitmap.Save(std::wstring(filePath.begin(), filePath.end()).c_str(), &clsidJpeg, NULL) == Ok;
}

// 保存为PNG格式
bool ImageProcessor::saveAsPNG(const std::string& filePath) {
    if (!isLoaded()) {
        return false;
    }

    // 使用GDI+保存图片
    Bitmap bitmap(hBitmap, NULL);
    CLSID clsidPng;
    GetEncoderClsid(L"image/png", &clsidPng);
    return bitmap.Save(std::wstring(filePath.begin(), filePath.end()).c_str(), &clsidPng, NULL) == Ok;
}

// 保存为BMP格式
bool ImageProcessor::saveAsBMP(const std::string& filePath) {
    if (!isLoaded()) {
        return false;
    }

    // 使用GDI+保存图片
    Bitmap bitmap(hBitmap, NULL);
    CLSID clsidBmp;
    GetEncoderClsid(L"image/bmp", &clsidBmp);
    return bitmap.Save(std::wstring(filePath.begin(), filePath.end()).c_str(), &clsidBmp, NULL) == Ok;
}

// 绘制文本水印
void ImageProcessor::drawTextWatermark(const Watermark& watermark) {
    if (!isLoaded()) {
        return;
    }

    // 创建GDI+图形对象
    Graphics graphics(hMemDC);

    // 设置文本属性
    FontFamily fontFamily(std::wstring(watermark.getFontName().begin(), watermark.getFontName().end()).c_str());
    int fontStyle = FontStyleRegular;
    if (watermark.getBold()) fontStyle |= FontStyleBold;
    if (watermark.getItalic()) fontStyle |= FontStyleItalic;
    Font font(&fontFamily, watermark.getFontSize(), fontStyle, UnitPixel);

    // 设置文本颜色
    Color watermarkColor(watermark.getColor().a, watermark.getColor().r, 
                         watermark.getColor().g, watermark.getColor().b);
    SolidBrush brush(watermarkColor);

    // 设置文本格式
    StringFormat stringFormat;
    stringFormat.SetAlignment(StringAlignmentNear);
    stringFormat.SetLineAlignment(StringAlignmentNear);

    // 转换文本为宽字符
    std::wstring text = std::wstring(watermark.getText().begin(), watermark.getText().end());

    // 计算文本大小
    RectF textRect;
    graphics.MeasureString(text.c_str(), text.length(), &font, PointF(0, 0), &stringFormat, &textRect);

    // 保存图形状态
    graphics.Save();

    // 设置旋转
    graphics.TranslateTransform(watermark.getPositionX() + textRect.Width / 2, 
                               watermark.getPositionY() + textRect.Height / 2);
    graphics.RotateTransform(watermark.getRotationAngle());

    // 绘制文本
    graphics.DrawString(text.c_str(), text.length(), &font, 
                       PointF(-textRect.Width / 2, -textRect.Height / 2), 
                       &stringFormat, &brush);

    // 恢复图形状态
    graphics.Restore();
}

// 释放资源
void ImageProcessor::releaseResources() {
    if (hBitmap) {
        DeleteObject(hBitmap);
        hBitmap = NULL;
    }
    if (hMemDC) {
        DeleteDC(hMemDC);
        hMemDC = NULL;
    }
    width = 0;
    height = 0;
    filePath.clear();
    hasAlphaChannel = false;
}

// 获取GDI+编码器CLSID
int GetEncoderClsid(const WCHAR* format, CLSID* pClsid) {
    UINT num = 0;          // 编码器数量
    UINT size = 0;         // 所需缓冲区大小

    ImageCodecInfo* pImageCodecInfo = NULL;

    // 获取编码器数量
    GetImageEncodersSize(&num, &size);
    if (size == 0) {
        return -1;  // 失败
    }

    // 分配缓冲区
    pImageCodecInfo = (ImageCodecInfo*)(malloc(size));
    if (pImageCodecInfo == NULL) {
        return -1;  // 失败
    }

    // 获取编码器信息
    GetImageEncoders(num, size, pImageCodecInfo);

    // 查找指定格式的编码器
    for (UINT j = 0; j < num; ++j) {
        if (wcscmp(pImageCodecInfo[j].MimeType, format) == 0) {
            *pClsid = pImageCodecInfo[j].Clsid;
            free(pImageCodecInfo);
            return j;  // 成功
        }
    }

    free(pImageCodecInfo);
    return -1;  // 未找到
}