// FileHandler.h - 文件处理类头文件
#ifndef FILEHANDLER_H
#define FILEHANDLER_H

#include <string>
#include <vector>
#include "core/ImageProcessor.h"

// 导出命名规则枚举
enum class ExportNamingRule {
    KEEP_ORIGINAL,      // 保留原文件名
    ADD_PREFIX,         // 添加前缀
    ADD_SUFFIX          // 添加后缀
};

// 文件处理类 - 负责文件的导入、导出和命名规则处理
class FileHandler {
private:
    std::string customPrefix;  // 自定义前缀
    std::string customSuffix;  // 自定义后缀

public:
    // 构造函数和析构函数
    FileHandler();
    ~FileHandler();

    // 导入文件
    std::vector<std::string> importFiles(const std::string& initialDirectory = "");
    
    // 导入文件夹
    std::vector<std::string> importFolder(const std::string& initialDirectory = "");
    
    // 导出文件
bool exportFile(const ImageProcessor& processor, const std::string& outputFolder, 
                const ExportNamingRule& rule, ImageFormat format);
    
    // 批量导出文件
bool batchExportFiles(const std::vector<ImageProcessor*>& processors, 
                      const std::string& outputFolder, 
                      const ExportNamingRule& rule, ImageFormat format);

    // 设置和获取自定义前缀
    void setCustomPrefix(const std::string& prefix);
    std::string getCustomPrefix() const;

    // 设置和获取自定义后缀
    void setCustomSuffix(const std::string& suffix);
    std::string getCustomSuffix() const;

    // 验证输出路径是否安全（不会覆盖原图）
bool validateOutputPath(const std::string& outputPath, const std::string& originalPath);

    // 获取文件保存对话框
bool getSaveFilePath(std::string& filePath, const std::string& defaultName, 
                     ImageFormat format, const std::string& initialDirectory = "");

    // 获取文件夹选择对话框
bool getSelectFolderPath(std::string& folderPath, const std::string& initialDirectory = "");

    // 获取文件选择对话框
bool getOpenFilePaths(std::vector<std::string>& filePaths, 
                      const std::string& initialDirectory = "");

    // 检查文件是否为支持的图片格式
bool isSupportedImageFormat(const std::string& filePath);

    // 获取支持的图片格式过滤器字符串
    std::string getImageFormatFilter();

private:
    // 内部辅助方法
    std::string generateOutputFileName(const std::string& originalFileName, 
                                     const ExportNamingRule& rule);
    
    std::string getFileExtension(ImageFormat format);
    
    std::string getFileNameWithoutExtension(const std::string& filePath);
    
    std::string getFileExtension(const std::string& filePath);
};

#endif // FILEHANDLER_H