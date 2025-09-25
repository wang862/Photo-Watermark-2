@echo off

REM Photo-Watermark-2 构建脚本
REM 这个批处理文件用于快速构建项目

REM 设置中文显示
chcp 65001

REM 检查是否有Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python环境。请先安装Python 3.7或更高版本。
    pause
    exit /b 1
)

REM 检查是否有pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到pip工具。
    pause
    exit /b 1
)

REM 安装依赖
echo 正在安装项目依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败。
    pause
    exit /b 1
)

REM 运行测试
choice /c YN /m "是否运行测试? (Y/N)" 
if %errorlevel% EQU 1 (
    echo 正在运行测试...
    python -m unittest discover tests
    if errorlevel 1 (
        echo 错误: 测试失败。
        pause
        exit /b 1
    )
)

REM 构建可执行文件
choice /c YN /m "是否构建可执行文件? (Y/N)" 
if %errorlevel% EQU 1 (
    echo 正在安装cx_Freeze...
    pip install cx_Freeze
    if errorlevel 1 (
        echo 错误: cx_Freeze安装失败。
        pause
        exit /b 1
    )
    
    echo 正在构建可执行文件...
    python setup.py build_exe
    if errorlevel 1 (
        echo 错误: 可执行文件构建失败。
        pause
        exit /b 1
    )
    
    echo 可执行文件已构建完成，位于dist目录下。
)

REM 完成提示
echo 构建完成!
pause