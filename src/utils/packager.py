from typing import List, Optional, Dict
import subprocess
import os
import sys
import logging
from pathlib import Path
import tempfile

class PyInstaller:
    """
    PyInstaller打包工具的封装类。
    提供简化的接口来执行Python项目的打包操作。
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        初始化PyInstaller封装类。

        Args:
            logger: 可选的logger对象，用于日志记录
        """
        self.logger = logger or logging.getLogger(__name__)
        
    def build(self,
              script_path: str,
              output_dir: str,
              onefile: bool = True,
              venv_path: Optional[str] = None,
              icon_path: Optional[str] = None,
              extra_files: Optional[List[str]] = None,
              version_file: Optional[str] = None) -> None:
        """
        执行打包操作。
        通过创建批处理文件并在新的cmd窗口中执行来实现打包过程的可视化。
        """
        try:
            # 准备工作目录（主脚本所在目录）
            work_dir = os.path.dirname(os.path.abspath(script_path))
            self.logger.info(f"工作目录: {work_dir}")
            
            # 如果有版本信息文件，读取产品名称和版本号
            output_name = None
            if version_file:
                try:
                    from utils.version_parser import VersionParser
                    parser = VersionParser(self.logger)
                    version_info = parser.parse_version_file(version_file)
                    product_name = version_info.get('ProductName', '').strip()
                    product_version = version_info.get('ProductVersion', '').strip()
                    if product_name and product_version:
                        # 移除版本号中的点号，使用下划线连接
                        version_str = product_version.replace('.', '_')
                        output_name = f"{product_name}_v{version_str}"
                        self.logger.info(f"使用版本信息命名: {output_name}")
                except Exception as e:
                    self.logger.warning(f"读取版本信息失败，使用默认名称: {str(e)}")
            
            # 构建命令
            if os.name == 'nt':  # Windows
                cmd = self._build_windows_command(
                    script_path=script_path,
                    output_dir=output_dir,
                    onefile=onefile,
                    venv_path=venv_path,
                    icon_path=icon_path,
                    extra_files=extra_files,
                    version_file=version_file,
                    output_name=output_name
                )
                
                # 创建临时批处理文件
                bat_content = f"""
@echo off
chcp 65001 > nul
cd /d "{work_dir}"
{cmd}
echo.
echo 打包完成，按任意键关闭窗口...
pause >nul
"""
                # 使用临时文件
                with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False, encoding='utf-8') as f:
                    f.write(bat_content)
                    bat_file = f.name
                
                self.logger.info(f"执行打包命令: {cmd}")
                
                # 在新窗口中执行批处理文件，使用UTF-8编码
                process = subprocess.Popen(
                    f'start cmd /k "chcp 65001>nul && {bat_file} & del {bat_file}"',
                    shell=True,
                    cwd=work_dir
                )
                
                # 等待进程启动
                process.wait()
                
            else:  # Linux/Mac
                # Unix系统的实现（如果需要的话）
                pass
                
        except Exception as e:
            self.logger.error(f"打包过程中出现错误: {str(e)}")
            raise
            
    def _build_windows_command(self, **kwargs) -> str:
        """构建Windows平台的命令"""
        script_path = kwargs['script_path']
        venv_path = kwargs.get('venv_path')
        output_name = kwargs.get('output_name')
        
        # 基础命令部分
        cmd_parts = []
        
        # 如果指定了虚拟环境，先激活它
        if venv_path:
            activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
            if not os.path.exists(activate_script):
                raise FileNotFoundError(f"虚拟环境激活脚本不存在: {activate_script}")
            cmd_parts.append(f'call "{activate_script}" &&')
        
        # 添加pyinstaller命令
        cmd_parts.append('pyinstaller')
        
        # 添加选项
        if kwargs.get('onefile'):
            cmd_parts.append('--onefile')
        else:
            cmd_parts.append('--onedir')
            
        cmd_parts.extend(['--distpath', f'"{kwargs["output_dir"]}"'])
        
        # 设置输出文件名
        if output_name:
            cmd_parts.extend(['--name', f'"{output_name}"'])
        
        if kwargs.get('icon_path'):
            cmd_parts.extend(['--icon', f'"{kwargs["icon_path"]}"'])
            
        if kwargs.get('version_file'):
            cmd_parts.extend(['--version-file', f'"{kwargs["version_file"]}"'])
            
        if kwargs.get('extra_files'):
            for file in kwargs['extra_files']:
                cmd_parts.extend(['--add-data', f'"{file};."'])
        
        # 添加主脚本
        cmd_parts.append(f'"{script_path}"')
        
        return ' '.join(cmd_parts)
        
    def _build_unix_command(self, **kwargs) -> str:
        """构建Unix平台的命令"""
        script_path = kwargs['script_path']
        venv_path = kwargs.get('venv_path')
        
        # 基础命令部分
        cmd_parts = []
        
        # 如果指定了虚拟环境，先激活它
        if venv_path:
            activate_script = os.path.join(venv_path, 'bin', 'activate')
            if not os.path.exists(activate_script):
                raise FileNotFoundError(f"虚拟环境激活脚本不存在: {activate_script}")
            cmd_parts.append(f'source "{activate_script}" &&')
        
        # 添加pyinstaller命令
        cmd_parts.append('pyinstaller')
        
        # 添加选项
        if kwargs.get('onefile'):
            cmd_parts.append('--onefile')
        else:
            cmd_parts.append('--onedir')
            
        cmd_parts.extend(['--distpath', f'"{kwargs["output_dir"]}"'])
        
        if kwargs.get('icon_path'):
            cmd_parts.extend(['--icon', f'"{kwargs["icon_path"]}"'])
            
        if kwargs.get('version_file'):
            cmd_parts.extend(['--version-file', f'"{kwargs["version_file"]}"'])
            
        if kwargs.get('extra_files'):
            for file in kwargs['extra_files']:
                cmd_parts.extend(['--add-data', f'"{file}:."'])
        
        # 添加主脚本
        cmd_parts.append(f'"{script_path}"')
        
        return ' '.join(cmd_parts) 