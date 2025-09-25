@echo off

REM Photo-Watermark-2 启动脚本
REM 版本: 1.0.0

cls
echo ========================================================
echo                    Photo-Watermark-2
                  图片水印工具 - 可执行版
echo ========================================================
echo.
echo 程序信息:
echo - 版本: 1.0.0
echo - 架构: 64位Windows可执行文件
echo - 打包工具: PyInstaller (onefile模式)
echo.
echo 程序位置:
echo %~dp0\dist\PhotoWatermark2.exe
echo.
echo 程序大小:
for %%I in (dist\PhotoWatermark2.exe) do echo %%~zI 字节
echo.
echo 使用说明:
echo 1. 此程序包含所有必要的依赖项，无需安装Python环境
echo 2. 直接双击即可运行，不会显示控制台窗口
echo 3. 如有问题，请确认您的Windows系统版本兼容
echo.
echo ========================================================
echo 按任意键启动程序...
pause >nul

echo 正在启动Photo-Watermark-2程序...
start "Photo-Watermark-2" "dist\PhotoWatermark2.exe"

REM 等待程序启动
ping -n 2 127.0.0.1 >nul

echo 启动完成！程序已在后台运行。
echo 按任意键退出此窗口...
pause >nul