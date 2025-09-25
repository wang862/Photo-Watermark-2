# Photo-Watermark-2

## 项目简介
Photo-Watermark-2 是一款功能强大、易于使用的图片水印工具，支持添加文本水印到图片上，并提供多种自定义选项。

## 功能特点

### 水印功能
- 支持添加自定义文本水印
- 可调整水印字体、大小、颜色和透明度
- 支持设置水印位置（居中、平铺、自定义坐标）
- 可调整水印旋转角度
- 支持设置水印间距

### 图片处理
- 支持单张图片和批量图片处理
- 支持多种图片格式（PNG、JPG、BMP等）
- 提供图片预览功能
- 可调整保存图片的质量

### 模板管理
- 支持保存水印设置为模板
- 可加载、重命名、删除模板
- 支持导入导出模板文件

### 用户体验
- 友好的图形界面
- 支持中文显示
- 保存用户配置
- 提供操作提示

## 系统要求

- Python 3.7 或更高版本
- PyQt5 5.15.0 或更高版本
- Pillow 9.0.0 或更高版本

## 安装方法

### 方法一：使用pip安装
1. 确保已安装Python 3.7或更高版本
2. 克隆或下载本项目
3. 打开命令行，进入项目目录
4. 执行以下命令安装依赖：
   ```
   pip install -r requirements.txt
   ```
5. 运行主程序：
   ```
   python src/main/main.py
   ```

### 方法二：使用构建脚本
1. 确保已安装Python 3.7或更高版本
2. 克隆或下载本项目
3. 双击运行 `build.bat` 文件
4. 按照提示完成安装和构建

## 使用说明

### 基本使用
1. 启动程序后，点击 "导入图片" 按钮选择一张或多张图片
2. 在水印设置区域，输入水印文本并调整相关参数
3. 通过预览窗口查看效果
4. 点击 "应用水印" 按钮选择输出目录并保存处理后的图片

### 批量处理
1. 点击 "导入图片" 按钮选择多张图片或整个文件夹
2. 设置好水印参数
3. 点击 "批量处理" 按钮选择输出目录
4. 程序将自动处理所有图片并保存

### 模板管理
1. 设置好水印参数后，点击 "保存模板" 按钮
2. 输入模板名称，点击 "确定"
3. 下次使用时，点击 "加载模板" 按钮选择保存的模板

## 项目结构

```
Photo-Watermark-2/
├── src/
│   ├── main/
│   │   └── main.py        # 主程序入口
│   ├── core/
│   │   ├── watermark.py       # 水印处理核心模块
│   │   ├── image_processor.py # 图像处理器模块
│   │   ├── file_handler.py    # 文件处理模块
│   │   └── template_manager.py # 模板管理模块
│   ├── ui/
│   │   ├── main_window.py     # 主窗口UI
│   │   ├── preview_widget.py  # 预览窗口组件
│   │   └── image_list_widget.py # 图片列表UI组件
│   ├── utils/
│   │   ├── config_manager.py  # 配置管理模块
│   │   └── common_utils.py    # 通用工具函数
│   └── resources/
│       └── icons/             # 图标资源
├── tests/
│   ├── test_watermark.py      # 水印模块测试
│   ├── test_image_processor.py # 图像处理器模块测试
│   ├── test_file_handler.py   # 文件处理模块测试
│   └── test_template_manager.py # 模板管理模块测试
├── requirements.txt           # 项目依赖
├── setup.py                   # 项目安装配置
├── build.bat                  # 构建脚本
└── README.md                  # 项目说明文档
```

## 开发说明

### 开发环境搭建
1. 克隆本项目
2. 安装开发依赖：`pip install -r requirements.txt`
3. 安装测试依赖：`pip install unittest`

### 运行测试
```
python -m unittest discover tests
```

### 构建可执行文件
```
python setup.py build_exe
```

## 许可证
本项目采用 MIT 许可证。

## 致谢
感谢所有为项目做出贡献的开发者。
