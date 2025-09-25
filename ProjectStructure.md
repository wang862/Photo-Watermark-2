# 图片水印工具项目结构设计

## 1. 项目概述
本项目是一款Windows平台上的图片水印工具，使用C++语言开发，无需安装额外第三方库。根据PRD文档，项目需要实现图片导入导出、文本水印添加、水印样式调整、实时预览和模板管理等功能。

## 2. 整体架构设计
采用模块化设计，将不同功能划分为独立模块，便于开发、测试和维护。整体架构如下：

```
Photo-Watermark-2/
├── src/                 # 源代码目录
│   ├── main/            # 主程序相关代码
│   ├── ui/              # 用户界面相关代码
│   ├── core/            # 核心功能实现
│   ├── utils/           # 工具类和辅助函数
│   └── resources/       # 资源文件
├── include/             # 头文件目录
├── build/               # 构建输出目录
├── docs/                # 文档目录
├── tests/               # 测试代码
├── PRD.md               # 产品需求文档
├── README.md            # 项目说明文档
└── .gitignore           # Git忽略文件
```

## 3. 模块划分与职责

### 3.1 主程序模块 (main)
- **main.cpp**: 程序入口点，负责初始化应用程序和启动主窗口
- **AppManager.cpp/AppManager.h**: 应用程序管理器，负责协调各个模块的工作

### 3.2 用户界面模块 (ui)
- **MainWindow.cpp/MainWindow.h**: 主窗口类，实现整个应用的界面布局
- **ImageListView.cpp/ImageListView.h**: 图片列表控件，显示已导入的图片缩略图和文件名
- **WatermarkSettingsPanel.cpp/WatermarkSettingsPanel.h**: 水印设置面板，包含文本输入、字体选择等控件
- **PositionSettingsPanel.cpp/PositionSettingsPanel.h**: 位置设置面板，包含预设位置按钮和旋转控制
- **FileOperationPanel.cpp/FileOperationPanel.h**: 文件操作面板，包含导入、导出按钮和命名规则设置
- **TemplateManagerPanel.cpp/TemplateManagerPanel.h**: 模板管理面板，实现模板的保存、加载和删除功能

### 3.3 核心功能模块 (core)
- **ImageProcessor.cpp/ImageProcessor.h**: 图像处理核心类，负责图片的加载、保存和水印添加
- **WatermarkGenerator.cpp/WatermarkGenerator.h**: 水印生成器，负责根据用户设置生成水印
- **TemplateManager.cpp/TemplateManager.h**: 模板管理器，负责模板的序列化和反序列化
- **FileHandler.cpp/FileHandler.h**: 文件处理类，负责文件的导入、导出和命名规则处理

### 3.4 工具模块 (utils)
- **StringUtils.cpp/StringUtils.h**: 字符串处理工具类
- **ImageUtils.cpp/ImageUtils.h**: 图像处理工具函数
- **ConfigUtils.cpp/ConfigUtils.h**: 配置文件处理工具类
- **ErrorHandler.cpp/ErrorHandler.h**: 错误处理工具类
- **ResourceManager.cpp/ResourceManager.h**: 资源管理工具类

## 4. 关键类设计

### 4.1 ImageProcessor 类
- **主要职责**: 负责图片的加载、保存和水印添加
- **关键方法**: 
  - `loadImage(const std::string& filePath)`: 加载图片文件
  - `saveImage(const std::string& filePath, ImageFormat format)`: 保存图片到指定路径
  - `applyWatermark(const Watermark& watermark)`: 应用水印到图片上
  - `getPreview()`: 获取预览图片

### 4.2 Watermark 类
- **主要职责**: 表示水印的各种属性
- **关键属性**: 
  - `text`: 水印文本内容
  - `fontName`, `fontSize`, `isBold`, `isItalic`: 字体相关属性
  - `color`: 水印颜色
  - `opacity`: 透明度
  - `positionX`, `positionY`: 位置坐标
  - `rotationAngle`: 旋转角度

### 4.3 TemplateManager 类
- **主要职责**: 管理水印模板的保存、加载和删除
- **关键方法**: 
  - `saveTemplate(const std::string& name, const WatermarkSettings& settings)`: 保存模板
  - `loadTemplate(const std::string& name)`: 加载模板
  - `deleteTemplate(const std::string& name)`: 删除模板
  - `getTemplateList()`: 获取模板列表

### 4.4 FileHandler 类
- **主要职责**: 处理文件导入导出和命名规则
- **关键方法**: 
  - `importFiles(const std::vector<std::string>& filePaths)`: 导入文件
  - `importFolder(const std::string& folderPath)`: 导入文件夹
  - `exportFile(const Image& image, const std::string& outputFolder, const std::string& originalFileName, const ExportNamingRule& rule)`: 导出文件
  - `validateOutputPath(const std::string& outputPath, const std::string& originalPath)`: 验证输出路径是否安全

## 5. 数据流设计
1. **图片导入流程**: 用户通过拖拽或文件选择器导入图片 → FileHandler 处理文件 → ImageProcessor 加载图片 → 显示在 ImageListView
2. **水印设置流程**: 用户在界面上调整水印设置 → Watermark 对象更新 → WatermarkGenerator 生成新水印 → ImageProcessor 应用水印 → 实时显示在预览区域
3. **模板管理流程**: 用户保存模板 → TemplateManager 将水印设置序列化保存 → 用户加载模板 → TemplateManager 反序列化并应用到当前设置
4. **图片导出流程**: 用户选择导出选项 → FileHandler 处理命名规则 → ImageProcessor 处理图片 → 保存到指定位置

## 6. 配置文件设计
- **模板配置文件**: 使用XML或JSON格式保存模板信息
- **应用配置文件**: 保存程序启动时的默认设置和上次关闭时的状态

## 7. 技术选型
- **开发语言**: C++11/14
- **UI框架**: Windows API (Win32)
- **图像处理**: Windows GDI+/WIC (Windows Imaging Component)
- **构建工具**: CMake
- **版本控制**: Git

## 8. 开发计划
1. **第一阶段**: 搭建基本框架，实现图片导入导出功能
2. **第二阶段**: 实现水印添加和基本样式设置
3. **第三阶段**: 实现实时预览和位置调整功能
4. **第四阶段**: 实现模板管理功能
5. **第五阶段**: 测试、优化和文档完善