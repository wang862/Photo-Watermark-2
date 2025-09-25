@echo off

REM 查看dist目录内容
echo 查看dist目录内容...
dir /s /b dist

echo.
echo 按任意键启动PhotoWatermark程序...
pause >nul

echo 启动PhotoWatermark程序...
start "PhotoWatermark" "dist\PhotoWatermark3.exe"