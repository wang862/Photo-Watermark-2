@echo off
REM Batch file to create PhotoWatermark executable

chcp 65001 >nul

 echo Starting executable creation process...

echo Current directory: %CD%

echo Checking Python installation...
python --version

echo Checking PyInstaller installation...
pip show pyinstaller

echo Creating dist directory if it doesn't exist...
mkdir dist 2>nul

echo Running PyInstaller command...
pyinstaller --onefile --windowed src\main\main.py --name=PhotoWatermark

echo Checking dist directory contents...
dir dist

echo Process completed!