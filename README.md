# Python Project Packager / Python项目打包工具

[English](#english) | [中文](#chinese)

## English

### Introduction
Python Project Packager is a GUI tool designed to simplify the process of packaging Python projects into executable files using PyInstaller. It provides a user-friendly interface with modern design and comprehensive features. The actual packaging process is executed in a separate CMD window, allowing you to monitor the progress in real-time.

### Features
- Easy-to-use graphical interface
- Support for single-file and directory mode packaging
- Virtual environment integration
- Automatic project file scanning
- Icon conversion (supports PNG, JPG to ICO)
- Version information management
- Additional files packaging
- Real-time packaging progress in CMD window
- Detailed logging

### Requirements
- Python 3.6+
- PyInstaller
- Pillow (PIL)
- tkinter (usually comes with Python)

### Installation
1. Clone or download this repository
2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage
1. Run the program:
```bash
python src/main.py
```

2. Basic Steps:
   - Select your main Python script
   - Choose output directory
   - Configure packaging options
   - (Optional) Select virtual environment
   - (Optional) Add icon file
   - (Optional) Configure version information
   - (Optional) Add additional files
   - Click "Start Packaging"
   - Monitor progress in the new CMD window

### Packaging Process
When you click "Start Packaging", the program will:
1. Open a new CMD window
2. Activate the virtual environment (if selected)
3. Execute PyInstaller with your configuration
4. Show real-time packaging progress
5. Keep the window open until packaging is complete
6. Display the final result and wait for your confirmation

### Version Information
You can create or edit version information in the GUI. The program will automatically look for `versionmark.txt` in the main script's directory. The generated executable will be named according to the product name and version in the version information.

### 注意事项
- 建议在虚拟环境中运行程序
- 确保所有路径不包含中文字符
- 打包过程中请保持CMD窗口开启
- 可以在CMD窗口中查看实时进度
- 可以在logs目录下查看详细日志

---

## Chinese

### 简介
Python项目打包工具是一个基于GUI的工具，旨在简化使用PyInstaller将Python项目打包成可执行文件的过程。它提供了现代化的用户界面和全面的功能。实际的打包过程会在单独的CMD窗口中执行，让你能够实时监控打包进度。

### 功能特点
- 简单易用的图形界面
- 支持单文件和目录模式打包
- 虚拟环境集成
- 自动项目文件扫描
- 图标转换（支持PNG、JPG转ICO）
- 版本信息管理
- 额外文件打包
- CMD窗口实时显示打包进度
- 详细的日志记录

### 环境要求
- Python 3.6+
- PyInstaller
- Pillow (PIL)

### 安装步骤
1. 克隆或下载此仓库
2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. 安装依赖：
```bash
pip install -r requirements.txt
```

### 使用方法
1. 运行程序：
```bash
python src/main.py
```

2. 基本步骤：
   - 选择主Python脚本
   - 选择输出目录
   - 配置打包选项
   - （可选）选择虚拟环境
   - （可选）添加图标文件
   - （可选）配置版本信息
   - （可选）添加额外文件
   - 点击"开始打包"
   - 在新打开的CMD窗口中监控进度

### 打包过程
当你点击"开始打包"时，程序会：
1. 打开一个新的CMD窗口
2. 激活虚拟环境（如果已选择）
3. 使用你的配置执行PyInstaller
4. 实时显示打包进度
5. 打包完成前保持窗口打开
6. 显示最终结果并等待确认

### 版本信息
你可以在GUI中创建或编辑版本信息。程序会自动在主脚本目录下查找`versionmark.txt`。生成的可执行文件将根据版本信息中的产品名称和版本号进行命名。

### 注意事项
- 建议在虚拟环境中运行程序
- 确保所有路径不包含中文字符
- 打包过程中请保持CMD窗口开启
- 可以在CMD窗口中查看实时进度
- 可以在logs目录下查看详细日志
