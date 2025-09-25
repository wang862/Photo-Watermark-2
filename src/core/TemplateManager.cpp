// TemplateManager.cpp - 模板管理类实现
#include "TemplateManager.h"
#include <windows.h>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <filesystem>
#include <algorithm>
#include <shlobj.h>

namespace fs = std::filesystem;

// 构造函数
TemplateManager::TemplateManager() : defaultTemplateName("Default") {
    // 初始化模板文件夹路径
    char appDataPath[MAX_PATH];
    if (SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, 0, appDataPath) == S_OK) {
        templatesFolder = std::string(appDataPath) + "\\PhotoWatermark2\\Templates";
    } else {
        // 如果无法获取AppData路径，使用当前目录
        templatesFolder = ".\\Templates";
    }
}

// 析构函数
TemplateManager::~TemplateManager() {
    // 析构函数不需要特殊处理
}

// 初始化模板管理器
bool TemplateManager::initialize() {
    // 确保模板文件夹存在
    if (!ensureTemplatesFolderExists()) {
        return false;
    }

    // 加载所有模板
    templates.clear();

    try {
        if (fs::exists(templatesFolder) && fs::is_directory(templatesFolder)) {
            for (const auto& entry : fs::directory_iterator(templatesFolder)) {
                if (entry.is_regular_file() && entry.path().extension() == ".tpl") {
                    std::string fileName = entry.path().filename().string();
                    std::string templateName = fileName.substr(0, fileName.length() - 4); // 移除.tpl扩展名

                    Watermark watermark;
                    if (loadTemplate(templateName, watermark)) {
                        templates[templateName] = watermark;
                    }
                }
            }
        }

        // 如果没有默认模板，创建一个
        if (!templateExists(defaultTemplateName)) {
            Watermark defaultWatermark;
            saveTemplate(defaultTemplateName, defaultWatermark, "默认模板");
        }

        return true;
    } catch (const std::exception& e) {
        return false;
    }
}

// 保存模板
bool TemplateManager::saveTemplate(const std::string& name, const Watermark& watermark, const std::string& description) {
    try {
        // 确保模板文件夹存在
        if (!ensureTemplatesFolderExists()) {
            return false;
        }

        // 清理模板名称
        std::string sanitizedName = sanitizeTemplateName(name);
        if (sanitizedName.empty()) {
            return false;
        }

        // 获取模板文件路径
        std::string filePath = getTemplateFilePath(sanitizedName);

        // 打开文件进行写入
        std::ofstream file(filePath);
        if (!file.is_open()) {
            return false;
        }

        // 写入模板头部信息
        file << "[Template]" << std::endl;
        file << "Name=" << sanitizedName << std::endl;
        file << "Description=" << description << std::endl;
        file << "LastModified=" << getCurrentDateTimeString() << std::endl;
        file << "[" << std::endl;

        // 写入水印属性
        file << "Text=" << watermark.getText() << std::endl;
        file << "FontName=" << watermark.getFontName() << std::endl;
        file << "FontSize=" << watermark.getFontSize() << std::endl;
        file << "IsBold=" << (watermark.getBold() ? "true" : "false") << std::endl;
        file << "IsItalic=" << (watermark.getItalic() ? "true" : "false") << std::endl;
        
        Color color = watermark.getColor();
        file << "ColorR=" << color.r << std::endl;
        file << "ColorG=" << color.g << std::endl;
        file << "ColorB=" << color.b << std::endl;
        file << "ColorA=" << color.a << std::endl;
        
        file << "Opacity=" << watermark.getOpacity() << std::endl;
        file << "PositionX=" << watermark.getPositionX() << std::endl;
        file << "PositionY=" << watermark.getPositionY() << std::endl;
        file << "RotationAngle=" << watermark.getRotationAngle() << std::endl;

        // 写入模板尾部信息
        file << "]" << std::endl;

        file.close();

        // 更新模板映射表
        templates[sanitizedName] = watermark;

        return true;
    } catch (const std::exception& e) {
        return false;
    }
}

// 加载模板
bool TemplateManager::loadTemplate(const std::string& name, Watermark& watermark) {
    try {
        // 清理模板名称
        std::string sanitizedName = sanitizeTemplateName(name);
        if (sanitizedName.empty()) {
            return false;
        }

        // 检查模板是否在内存中
        auto it = templates.find(sanitizedName);
        if (it != templates.end()) {
            watermark = it->second;
            return true;
        }

        // 获取模板文件路径
        std::string filePath = getTemplateFilePath(sanitizedName);

        // 检查文件是否存在
        if (!fs::exists(filePath)) {
            return false;
        }

        // 打开文件进行读取
        std::ifstream file(filePath);
        if (!file.is_open()) {
            return false;
        }

        std::string line;
        bool inWatermarkSection = false;

        // 读取文件内容
        while (std::getline(file, line)) {
            // 跳过空行
            if (line.empty()) {
                continue;
            }

            // 检查是否进入水印属性部分
            if (line == "[") {
                inWatermarkSection = true;
                continue;
            }
            if (line == "]") {
                inWatermarkSection = false;
                break;
            }

            // 如果在水印属性部分，解析属性
            if (inWatermarkSection) {
                size_t equalsPos = line.find('=');
                if (equalsPos != std::string::npos) {
                    std::string key = line.substr(0, equalsPos);
                    std::string value = line.substr(equalsPos + 1);

                    // 解析各个属性
                    if (key == "Text") {
                        watermark.setText(value);
                    } else if (key == "FontName") {
                        watermark.setFontName(value);
                    } else if (key == "FontSize") {
                        watermark.setFontSize(std::stoi(value));
                    } else if (key == "IsBold") {
                        watermark.setBold(value == "true");
                    } else if (key == "IsItalic") {
                        watermark.setItalic(value == "true");
                    } else if (key == "ColorR") {
                        Color color = watermark.getColor();
                        color.r = std::stoi(value);
                        watermark.setColor(color);
                    } else if (key == "ColorG") {
                        Color color = watermark.getColor();
                        color.g = std::stoi(value);
                        watermark.setColor(color);
                    } else if (key == "ColorB") {
                        Color color = watermark.getColor();
                        color.b = std::stoi(value);
                        watermark.setColor(color);
                    } else if (key == "ColorA") {
                        Color color = watermark.getColor();
                        color.a = std::stoi(value);
                        watermark.setColor(color);
                    } else if (key == "Opacity") {
                        watermark.setOpacity(std::stof(value));
                    } else if (key == "PositionX") {
                        watermark.setPosition(std::stoi(value), watermark.getPositionY());
                    } else if (key == "PositionY") {
                        watermark.setPosition(watermark.getPositionX(), std::stoi(value));
                    } else if (key == "RotationAngle") {
                        watermark.setRotationAngle(std::stof(value));
                    }
                }
            }
        }

        file.close();

        // 更新模板映射表
        templates[sanitizedName] = watermark;

        return true;
    } catch (const std::exception& e) {
        return false;
    }
}

// 删除模板
bool TemplateManager::deleteTemplate(const std::string& name) {
    try {
        // 清理模板名称
        std::string sanitizedName = sanitizeTemplateName(name);
        if (sanitizedName.empty()) {
            return false;
        }

        // 不允许删除默认模板
        if (sanitizedName == defaultTemplateName) {
            return false;
        }

        // 获取模板文件路径
        std::string filePath = getTemplateFilePath(sanitizedName);

        // 删除文件
        if (fs::exists(filePath)) {
            if (!fs::remove(filePath)) {
                return false;
            }
        }

        // 从映射表中移除
        templates.erase(sanitizedName);

        return true;
    } catch (const std::exception& e) {
        return false;
    }
}

// 获取模板列表
std::vector<TemplateInfo> TemplateManager::getTemplateList() {
    std::vector<TemplateInfo> templateList;

    try {
        if (fs::exists(templatesFolder) && fs::is_directory(templatesFolder)) {
            for (const auto& entry : fs::directory_iterator(templatesFolder)) {
                if (entry.is_regular_file() && entry.path().extension() == ".tpl") {
                    std::string fileName = entry.path().filename().string();
                    std::string templateName = fileName.substr(0, fileName.length() - 4); // 移除.tpl扩展名

                    TemplateInfo info;
                    info.name = templateName;
                    info.description = "";
                    info.lastModified = "";

                    // 读取模板信息
                    std::string filePath = getTemplateFilePath(templateName);
                    std::ifstream file(filePath);
                    if (file.is_open()) {
                        std::string line;
                        while (std::getline(file, line)) {
                            if (line.empty()) continue;
                            if (line == "[") break;

                            size_t equalsPos = line.find('=');
                            if (equalsPos != std::string::npos) {
                                std::string key = line.substr(0, equalsPos);
                                std::string value = line.substr(equalsPos + 1);

                                if (key == "Description") {
                                    info.description = value;
                                } else if (key == "LastModified") {
                                    info.lastModified = value;
                                }
                            }
                        }
                        file.close();
                    }

                    templateList.push_back(info);
                }
            }
        }

        // 按名称排序
        std::sort(templateList.begin(), templateList.end(), [](const TemplateInfo& a, const TemplateInfo& b) {
            return a.name < b.name;
        });
    } catch (const std::exception& e) {
        // 发生异常时返回空列表
    }

    return templateList;
}

// 检查模板是否存在
bool TemplateManager::templateExists(const std::string& name) {
    // 检查内存中的模板
    auto it = templates.find(name);
    if (it != templates.end()) {
        return true;
    }

    // 检查文件系统中的模板
    std::string filePath = getTemplateFilePath(name);
    return fs::exists(filePath);
}

// 设置默认模板
void TemplateManager::setDefaultTemplate(const std::string& name) {
    if (templateExists(name)) {
        defaultTemplateName = name;
        // 保存应用程序设置，记录默认模板
        Watermark dummy;
        saveApplicationSettings(dummy);
    }
}

// 获取默认模板名称
std::string TemplateManager::getDefaultTemplate() const {
    return defaultTemplateName;
}

// 加载默认模板
bool TemplateManager::loadDefaultTemplate(Watermark& watermark) {
    return loadTemplate(defaultTemplateName, watermark);
}

// 保存应用程序设置
bool TemplateManager::saveApplicationSettings(const Watermark& lastUsedSettings) {
    try {
        // 确保模板文件夹存在
        if (!ensureTemplatesFolderExists()) {
            return false;
        }

        // 获取设置文件路径
        std::string filePath = getSettingsFilePath();

        // 打开文件进行写入
        std::ofstream file(filePath);
        if (!file.is_open()) {
            return false;
        }

        // 写入设置
        file << "[ApplicationSettings]" << std::endl;
        file << "DefaultTemplate=" << defaultTemplateName << std::endl;
        file << "AutoLoadLastUsedSettings=true" << std::endl;

        file.close();

        // 保存上次使用的设置
        autoSaveLastUsedSettings(lastUsedSettings);

        return true;
    } catch (const std::exception& e) {
        return false;
    }
}

// 加载应用程序设置
bool TemplateManager::loadApplicationSettings(Watermark& settings) {
    try {
        // 获取设置文件路径
        std::string filePath = getSettingsFilePath();

        // 检查文件是否存在
        if (!fs::exists(filePath)) {
            return false;
        }

        // 打开文件进行读取
        std::ifstream file(filePath);
        if (!file.is_open()) {
            return false;
        }

        std::string line;

        // 读取文件内容
        while (std::getline(file, line)) {
            if (line.empty()) continue;

            size_t equalsPos = line.find('=');
            if (equalsPos != std::string::npos) {
                std::string key = line.substr(0, equalsPos);
                std::string value = line.substr(equalsPos + 1);

                if (key == "DefaultTemplate") {
                    defaultTemplateName = value;
                } else if (key == "AutoLoadLastUsedSettings" && value == "true") {
                    // 自动加载上次使用的设置
                    autoLoadLastUsedSettings(settings);
                }
            }
        }

        file.close();

        return true;
    } catch (const std::exception& e) {
        return false;
    }
}

// 自动保存上次使用的设置
bool TemplateManager::autoSaveLastUsedSettings(const Watermark& settings) {
    return saveTemplate("__LastUsedSettings", settings, "上次使用的设置");
}

// 自动加载上次使用的设置
bool TemplateManager::autoLoadLastUsedSettings(Watermark& settings) {
    return loadTemplate("__LastUsedSettings", settings);
}

// 获取模板文件路径
std::string TemplateManager::getTemplateFilePath(const std::string& name) {
    return templatesFolder + "\\" + sanitizeTemplateName(name) + ".tpl";
}

// 获取设置文件路径
std::string TemplateManager::getSettingsFilePath() {
    return templatesFolder + "\\settings.ini";
}

// 获取上次使用的设置文件路径
std::string TemplateManager::getLastUsedSettingsFilePath() {
    return getTemplateFilePath("__LastUsedSettings");
}

// 获取当前日期时间字符串
std::string TemplateManager::getCurrentDateTimeString() {
    SYSTEMTIME st;
    GetLocalTime(&st);

    std::stringstream ss;
    ss << std::setw(4) << std::setfill('0') << st.wYear << "/"
       << std::setw(2) << std::setfill('0') << st.wMonth << "/"
       << std::setw(2) << std::setfill('0') << st.wDay << " "
       << std::setw(2) << std::setfill('0') << st.wHour << ":"
       << std::setw(2) << std::setfill('0') << st.wMinute << ":"
       << std::setw(2) << std::setfill('0') << st.wSecond;

    return ss.str();
}

// 确保模板文件夹存在
bool TemplateManager::ensureTemplatesFolderExists() {
    try {
        if (!fs::exists(templatesFolder)) {
            return fs::create_directories(templatesFolder);
        }
        return true;
    } catch (const std::exception& e) {
        return false;
    }
}

// 清理模板名称，移除非法字符
std::string TemplateManager::sanitizeTemplateName(const std::string& name) {
    std::string sanitized = name;

    // 移除非法文件名字符
    const std::string illegalChars = "\\/:*?\"<>|";
    for (char c : illegalChars) {
        sanitized.erase(std::remove(sanitized.begin(), sanitized.end(), c), sanitized.end());
    }

    // 移除前导和尾随空格
    size_t start = sanitized.find_first_not_of(" \	");
    size_t end = sanitized.find_last_not_of(" \	");
    if (start == std::string::npos || end == std::string::npos) {
        return "";
    }
    sanitized = sanitized.substr(start, end - start + 1);

    // 限制长度
    const size_t maxLength = 50;
    if (sanitized.length() > maxLength) {
        sanitized = sanitized.substr(0, maxLength);
    }

    return sanitized;
}