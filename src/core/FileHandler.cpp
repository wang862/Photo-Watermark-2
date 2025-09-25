// FileHandler.cpp - 文件处理类实现
#include "FileHandler.h"
#include <windows.h>
#include <string>
#include <vector>
#include <algorithm>
#include <shlwapi.h>
#include <filesystem>

#pragma comment(lib, "shlwapi.lib")

namespace fs = std::filesystem;

// 构造函数
FileHandler::FileHandler() : customPrefix("wm_"), customSuffix("_watermarked") {
}

// 析构函数
FileHandler::~FileHandler() {
}

// 导入文件
std::vector<std::string> FileHandler::importFiles(const std::string& initialDirectory) {
    std::vector<std::string> filePaths;
    if (getOpenFilePaths(filePaths, initialDirectory)) {
        return filePaths;
    }
    return filePaths;
}

// 导入文件夹
std::vector<std::string> FileHandler::importFolder(const std::string& initialDirectory) {
    std::vector<std::string> filePaths;
    std::string folderPath;
    
    if (getSelectFolderPath(folderPath, initialDirectory)) {
        try {
            if (fs::exists(folderPath) && fs::is_directory(folderPath)) {
                for (const auto& entry : fs::recursive_directory_iterator(folderPath)) {
                    if (entry.is_regular_file() && isSupportedImageFormat(entry.path().string())) {
                        filePaths.push_back(entry.path().string());
                    }
                }
            }
        } catch (const std::exception& e) {
            // 忽略异常，返回已收集的文件路径
        }
    }
    
    return filePaths;
}

// 导出文件
bool FileHandler::exportFile(const ImageProcessor& processor, const std::string& outputFolder, 
                            const ExportNamingRule& rule, ImageFormat format) {
    if (!processor.isLoaded()) {
        return false;
    }
    
    // 验证输出路径
    if (!validateOutputPath(outputFolder, processor.getFilePath())) {
        return false;
    }
    
    // 确保输出文件夹存在
    try {
        if (!fs::exists(outputFolder)) {
            if (!fs::create_directories(outputFolder)) {
                return false;
            }
        }
    } catch (const std::exception& e) {
        return false;
    }
    
    // 获取原始文件名
    std::string originalFileName = PathFindFileNameA(processor.getFilePath().c_str());
    
    // 生成输出文件名
    std::string outputFileName = generateOutputFileName(originalFileName, rule);
    
    // 添加文件扩展名
    std::string extension = getFileExtension(format);
    std::string outputFilePath = outputFolder + "\\" + outputFileName + extension;
    
    // 检查文件是否已存在，如果存在则添加数字后缀
    int counter = 1;
    std::string baseName = outputFileName;
    while (fs::exists(outputFilePath)) {
        outputFileName = baseName + "(" + std::to_string(counter) + ")";
        outputFilePath = outputFolder + "\\" + outputFileName + extension;
        counter++;
    }
    
    // 保存文件
    return processor.saveImage(outputFilePath, format);
}

// 批量导出文件
bool FileHandler::batchExportFiles(const std::vector<ImageProcessor*>& processors, 
                                  const std::string& outputFolder, 
                                  const ExportNamingRule& rule, ImageFormat format) {
    bool allSuccess = true;
    
    // 确保输出文件夹存在
    try {
        if (!fs::exists(outputFolder)) {
            if (!fs::create_directories(outputFolder)) {
                return false;
            }
        }
    } catch (const std::exception& e) {
        return false;
    }
    
    // 逐个导出文件
    for (const auto& processor : processors) {
        if (processor && processor->isLoaded()) {
            // 验证输出路径
            if (!validateOutputPath(outputFolder, processor->getFilePath())) {
                allSuccess = false;
                continue;
            }
            
            // 获取原始文件名
            std::string originalFileName = PathFindFileNameA(processor->getFilePath().c_str());
            
            // 生成输出文件名
            std::string outputFileName = generateOutputFileName(originalFileName, rule);
            
            // 添加文件扩展名
            std::string extension = getFileExtension(format);
            std::string outputFilePath = outputFolder + "\\" + outputFileName + extension;
            
            // 检查文件是否已存在，如果存在则添加数字后缀
            int counter = 1;
            std::string baseName = outputFileName;
            while (fs::exists(outputFilePath)) {
                outputFileName = baseName + "(" + std::to_string(counter) + ")";
                outputFilePath = outputFolder + "\\" + outputFileName + extension;
                counter++;
            }
            
            // 保存文件
            if (!processor->saveImage(outputFilePath, format)) {
                allSuccess = false;
            }
        } else {
            allSuccess = false;
        }
    }
    
    return allSuccess;
}

// 设置自定义前缀
void FileHandler::setCustomPrefix(const std::string& prefix) {
    customPrefix = prefix;
}

// 获取自定义前缀
std::string FileHandler::getCustomPrefix() const {
    return customPrefix;
}

// 设置自定义后缀
void FileHandler::setCustomSuffix(const std::string& suffix) {
    customSuffix = suffix;
}

// 获取自定义后缀
std::string FileHandler::getCustomSuffix() const {
    return customSuffix;
}

// 验证输出路径是否安全
bool FileHandler::validateOutputPath(const std::string& outputPath, const std::string& originalPath) {
    try {
        // 获取原始文件所在的文件夹
        fs::path originalFolder = fs::path(originalPath).parent_path();
        fs::path outputFolder = fs::path(outputPath);
        
        // 规范化路径（处理相对路径和符号链接）
        originalFolder = fs::canonical(originalFolder);
        outputFolder = fs::canonical(outputFolder);
        
        // 检查是否为同一文件夹
        return originalFolder != outputFolder;
    } catch (const std::exception& e) {
        // 如果发生异常（例如文件不存在或权限问题），返回false
        return false;
    }
}

// 获取文件保存对话框
bool FileHandler::getSaveFilePath(std::string& filePath, const std::string& defaultName, 
                                ImageFormat format, const std::string& initialDirectory) {
    OPENFILENAMEA ofn;
    char szFile[MAX_PATH] = {0};
    
    // 设置默认文件名
    if (!defaultName.empty()) {
        strcpy_s(szFile, defaultName.c_str());
    }
    
    // 初始化OPENFILENAME结构
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile);
    
    // 设置过滤器
    std::string filter;
    switch (format) {
    case ImageFormat::JPEG:
        filter = "JPEG Images (*.jpg;*.jpeg)\0*.jpg;*.jpeg\0All Files (*.*)\0*.*\0\0";
        break;
    case ImageFormat::PNG:
        filter = "PNG Images (*.png)\0*.png\0All Files (*.*)\0*.*\0\0";
        break;
    case ImageFormat::BMP:
        filter = "BMP Images (*.bmp)\0*.bmp\0All Files (*.*)\0*.*\0\0";
        break;
    default:
        filter = "All Files (*.*)\0*.*\0\0";
    }
    
    ofn.lpstrFilter = filter.c_str();
    ofn.nFilterIndex = 1;
    
    // 设置初始目录
    if (!initialDirectory.empty()) {
        ofn.lpstrInitialDir = initialDirectory.c_str();
    }
    
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrDefExt = getFileExtension(format).substr(1).c_str(); // 移除点号
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST | OFN_OVERWRITEPROMPT;
    
    // 显示保存对话框
    if (GetSaveFileNameA(&ofn) == TRUE) {
        filePath = ofn.lpstrFile;
        return true;
    }
    
    return false;
}

// 获取文件夹选择对话框
bool FileHandler::getSelectFolderPath(std::string& folderPath, const std::string& initialDirectory) {
    BROWSEINFOA bi;
    char szDisplayName[MAX_PATH] = {0};
    LPITEMIDLIST pidl;
    
    // 初始化BROWSEINFO结构
    ZeroMemory(&bi, sizeof(bi));
    bi.hwndOwner = NULL;
    bi.pidlRoot = NULL;
    bi.pszDisplayName = szDisplayName;
    bi.lpszTitle = "选择文件夹";
    bi.ulFlags = BIF_RETURNONLYFSDIRS | BIF_NEWDIALOGSTYLE;
    bi.lpfn = NULL;
    bi.lParam = 0;
    bi.iImage = 0;
    
    // 如果提供了初始目录，设置它
    if (!initialDirectory.empty()) {
        // 这个功能需要回调函数来设置初始目录，这里简化处理
    }
    
    // 显示文件夹选择对话框
    pidl = SHBrowseForFolderA(&bi);
    if (pidl != NULL) {
        // 获取选中的文件夹路径
        if (SHGetPathFromIDListA(pidl, szDisplayName)) {
            folderPath = szDisplayName;
            CoTaskMemFree(pidl);
            return true;
        }
        CoTaskMemFree(pidl);
    }
    
    return false;
}

// 获取文件选择对话框
bool FileHandler::getOpenFilePaths(std::vector<std::string>& filePaths, 
                                  const std::string& initialDirectory) {
    OPENFILENAMEA ofn;
    char szFile[MAX_PATH * 10] = {0}; // 增加缓冲区大小以支持多选
    
    // 初始化OPENFILENAME结构
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile);
    ofn.lpstrFilter = getImageFormatFilter().c_str();
    ofn.nFilterIndex = 1;
    
    // 设置初始目录
    if (!initialDirectory.empty()) {
        ofn.lpstrInitialDir = initialDirectory.c_str();
    }
    
    ofn.lpstrFileTitle = NULL;
    ofn.nMaxFileTitle = 0;
    ofn.lpstrDefExt = "jpg";
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST | OFN_ALLOWMULTISELECT | OFN_EXPLORER;
    
    // 显示打开文件对话框
    if (GetOpenFileNameA(&ofn) == TRUE) {
        // 处理多选结果
        char* p = szFile;
        std::string folderPath;
        
        // 第一个字符串是文件夹路径
        folderPath = p;
        p += folderPath.length() + 1;
        
        // 后续的字符串是文件名
        while (*p) {
            std::string fileName = p;
            filePaths.push_back(folderPath + "\\" + fileName);
            p += fileName.length() + 1;
        }
        
        // 如果只选择了一个文件，GetOpenFileName会直接返回完整路径
        if (filePaths.empty() && !folderPath.empty()) {
            filePaths.push_back(folderPath);
        }
        
        return true;
    }
    
    return false;
}

// 检查文件是否为支持的图片格式
bool FileHandler::isSupportedImageFormat(const std::string& filePath) {
    std::string extension = getFileExtension(filePath);
    std::transform(extension.begin(), extension.end(), extension.begin(), ::tolower);
    
    return (extension == ".jpg" || extension == ".jpeg" || 
            extension == ".png" || extension == ".bmp");
}

// 获取支持的图片格式过滤器字符串
std::string FileHandler::getImageFormatFilter() {
    return "All Supported Images (*.jpg;*.jpeg;*.png;*.bmp)\0*.jpg;*.jpeg;*.png;*.bmp\0" 
           "JPEG Images (*.jpg;*.jpeg)\0*.jpg;*.jpeg\0" 
           "PNG Images (*.png)\0*.png\0" 
           "BMP Images (*.bmp)\0*.bmp\0" 
           "All Files (*.*)\0*.*\0\0";
}

// 生成输出文件名
std::string FileHandler::generateOutputFileName(const std::string& originalFileName, 
                                              const ExportNamingRule& rule) {
    // 获取不带扩展名的文件名
    std::string baseName = getFileNameWithoutExtension(originalFileName);
    
    // 根据命名规则生成新文件名
    switch (rule) {
    case ExportNamingRule::KEEP_ORIGINAL:
        return baseName;
    case ExportNamingRule::ADD_PREFIX:
        return customPrefix + baseName;
    case ExportNamingRule::ADD_SUFFIX:
        return baseName + customSuffix;
    default:
        return baseName;
    }
}

// 获取文件扩展名（带点号）
std::string FileHandler::getFileExtension(ImageFormat format) {
    switch (format) {
    case ImageFormat::JPEG:
        return ".jpg";
    case ImageFormat::PNG:
        return ".png";
    case ImageFormat::BMP:
        return ".bmp";
    default:
        return ".jpg";
    }
}

// 获取不带扩展名的文件名
std::string FileHandler::getFileNameWithoutExtension(const std::string& filePath) {
    std::string fileName = PathFindFileNameA(filePath.c_str());
    size_t dotPos = fileName.find_last_of('.');
    if (dotPos != std::string::npos) {
        return fileName.substr(0, dotPos);
    }
    return fileName;
}

// 获取文件扩展名（带点号）
std::string FileHandler::getFileExtension(const std::string& filePath) {
    std::string fileName = PathFindFileNameA(filePath.c_str());
    size_t dotPos = fileName.find_last_of('.');
    if (dotPos != std::string::npos) {
        return fileName.substr(dotPos);
    }
    return "";
}