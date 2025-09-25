// ImageProcessor.h - 图像处理核心类头文件
#ifndef IMAGEPROCESSOR_H
#define IMAGEPROCESSOR_H

#include <string>
#include <vector>
#include <Windows.h>
#include "Watermark.h"

// 图片格式枚举
enum class ImageFormat {
    JPEG,
    PNG,
    BMP,
    UNKNOWN
};

// 图像处理核心类 - 负责图片的加载、保存和水印添加
class ImageProcessor {
private:
    HBITMAP hBitmap;        // 位图句柄
    HDC hMemDC;             // 内存DC
    int width;              // 图片宽度
    int height;             // 图片高度
    std::string filePath;   // 原图文件路径
    bool hasAlphaChannel;   // 是否有透明通道

public:
    // 构造函数和析构函数
    ImageProcessor();
    ~ImageProcessor();

    // 加载和保存图片
    bool loadImage(const std::string& filePath);
    bool saveImage(const std::string& filePath, ImageFormat format);

    // 从HBITMAP创建图片
    bool createFromHBITMAP(HBITMAP bitmap, int w, int h);

    // 应用水印
    bool applyWatermark(const Watermark& watermark);

    // 批量处理图片
    static bool batchProcessImages(const std::vector<std::string>& inputPaths,
                                  const std::string& outputFolder,
                                  const Watermark& watermark,
                                  ImageFormat outputFormat);

    // 获取图片信息
    int getWidth() const;
    int getHeight() const;
    HBITMAP getHBITMAP() const;
    bool hasAlpha() const;
    std::string getFilePath() const;

    // 预览相关
    HBITMAP getPreview(int previewWidth, int previewHeight);
    void releasePreview(HBITMAP hPreviewBitmap);

    // 辅助方法
    bool isLoaded() const;
    void clear();

private:
    // 内部辅助方法
    ImageFormat getFormatFromFileExtension(const std::string& filePath);
    bool saveAsJPEG(const std::string& filePath);
    bool saveAsPNG(const std::string& filePath);
    bool saveAsBMP(const std::string& filePath);
    void drawTextWatermark(const Watermark& watermark);
    void releaseResources();
};

#endif // IMAGEPROCESSOR_H