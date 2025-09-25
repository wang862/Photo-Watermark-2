@echo off
REM 测试PhotoWatermark可执行文件

echo 测试可执行文件是否存在...
if exist dist\PhotoWatermark.exe (
    echo 找到可执行文件！大小: %~z1 bytes
    echo. 
    echo 尝试运行可执行文件...
    start "" dist\PhotoWatermark.exe
    echo 程序已启动！
) else (
    echo 错误：未找到可执行文件！
)

pause