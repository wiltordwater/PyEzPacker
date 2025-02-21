from typing import List, Optional, Set
import os
import logging
from pathlib import Path

class ProjectScanner:
    """
    项目文件扫描器。
    用于自动识别项目中的相关文件。
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        初始化项目扫描器。

        Args:
            logger: 可选的logger对象，用于日志记录
        """
        self.logger = logger or logging.getLogger(__name__)
        
    def scan_project(self, main_script_path: str) -> dict:
        """
        扫描主脚本所在目录，识别相关文件。
        只扫描当前目录，不进入子目录。

        Args:
            main_script_path: 主脚本路径

        Returns:
            dict: 包含识别到的文件信息的字典
        """
        project_dir = Path(main_script_path).parent
        self.logger.info(f"开始扫描目录: {project_dir}")
        
        result = {
            'python_files': set(),
            'data_files': set(),
            'requirements': None,
            'version_file': None,
            'icon_file': None,
            'venv_dir': None
        }
        
        try:
            # 检查是否存在venv目录
            venv_path = project_dir / 'venv'
            if venv_path.exists() and venv_path.is_dir():
                result['venv_dir'] = str(venv_path)
            
            # 扫描当前目录中的文件
            for item in project_dir.iterdir():
                if not item.is_file():  # 跳过目录
                    continue
                    
                file_path = str(item)
                file_name = item.name.lower()  # 转换为小写以进行大小写不敏感的匹配
                
                # 优先识别versionmark.txt作为版本信息文件
                if file_name == 'versionmark.txt':
                    result['version_file'] = file_path
                    continue  # 跳过后续检查，不将其添加到data_files中
                
                # 识别Python文件
                if file_name.endswith('.py'):
                    result['python_files'].add(file_path)
                    
                # 识别requirements.txt
                elif file_name == 'requirements.txt':
                    result['requirements'] = file_path
                    
                # 识别图标文件
                elif file_name.endswith(('.ico', '.png', '.jpg', '.jpeg')):
                    if not result['icon_file']:  # 只使用找到的第一个图标文件
                        result['icon_file'] = file_path
                    
                # 识别其他可能需要打包的文件
                # 排除已识别的特殊文件
                elif (file_name.endswith(('.json', '.yaml', '.yml', '.xml', '.csv', '.txt')) 
                      and file_name not in ['requirements.txt', 'versionmark.txt']):
                    result['data_files'].add(file_path)
            
            self.logger.info(f"目录扫描完成，找到 {len(result['python_files'])} 个Python文件")
            if result['version_file']:
                self.logger.info(f"找到版本信息文件: {result['version_file']}")
            
        except Exception as e:
            self.logger.error(f"扫描目录时出错: {str(e)}")
            raise
            
        return result 