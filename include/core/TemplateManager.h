// TemplateManager.h - 模板管理类头文件
#ifndef TEMPLATEMANAGER_H
#define TEMPLATEMANAGER_H

#include <string>
#include <vector>
#include <map>
#include "Watermark.h"

// 模板信息结构
struct TemplateInfo {
    std::string name;          // 模板名称
    std::string description;   // 模板描述
    std::string lastModified;  // 最后修改时间
};

// 模板管理类 - 负责模板的序列化和反序列化
class TemplateManager {
private:
    std::string templatesFolder;  // 模板文件夹路径
    std::map<std::string, Watermark> templates;  // 模板映射表
    std::string defaultTemplateName;  // 默认模板名称

public:
    // 构造函数和析构函数
    TemplateManager();
    ~TemplateManager();

    // 初始化模板管理器
    bool initialize();

    // 保存模板
    bool saveTemplate(const std::string& name, const Watermark& watermark, const std::string& description = "");

    // 加载模板
    bool loadTemplate(const std::string& name, Watermark& watermark);

    // 删除模板
    bool deleteTemplate(const std::string& name);

    // 获取模板列表
    std::vector<TemplateInfo> getTemplateList();

    // 检查模板是否存在
bool templateExists(const std::string& name);

    // 设置和获取默认模板
    void setDefaultTemplate(const std::string& name);
    std::string getDefaultTemplate() const;
    bool loadDefaultTemplate(Watermark& watermark);

    // 保存和加载应用程序设置
    bool saveApplicationSettings(const Watermark& lastUsedSettings);
    bool loadApplicationSettings(Watermark& settings);

    // 自动保存和加载上次使用的设置
    bool autoSaveLastUsedSettings(const Watermark& settings);
    bool autoLoadLastUsedSettings(Watermark& settings);

private:
    // 内部辅助方法
    std::string getTemplateFilePath(const std::string& name);
    std::string getSettingsFilePath();
    std::string getLastUsedSettingsFilePath();
    std::string getCurrentDateTimeString();
    bool ensureTemplatesFolderExists();
    std::string sanitizeTemplateName(const std::string& name);
};

#endif // TEMPLATEMANAGER_H