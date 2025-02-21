from typing import Dict, Optional, Tuple
import re
import ast
import logging
from pathlib import Path

class VersionParser:
    """
    版本信息文件解析器。
    支持读取和解析PyInstaller格式的版本信息文件。
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        初始化版本信息解析器。

        Args:
            logger: 可选的logger对象，用于日志记录
        """
        self.logger = logger or logging.getLogger(__name__)
        
    def parse_version_file(self, file_path: str) -> Dict[str, str]:
        """
        解析版本信息文件。

        Args:
            file_path: 版本信息文件路径

        Returns:
            Dict[str, str]: 版本信息字典

        Raises:
            FileNotFoundError: 文件不存在时抛出
            ValueError: 文件格式错误时抛出
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取版本信息
            version_info = {
                'filevers': self._extract_tuple(content, 'filevers'),
                'prodvers': self._extract_tuple(content, 'prodvers'),
                'CompanyName': self._extract_string(content, 'CompanyName'),
                'FileDescription': self._extract_string(content, 'FileDescription'),
                'FileVersion': self._extract_string(content, 'FileVersion'),
                'LegalCopyright': self._extract_string(content, 'LegalCopyright'),
                'ProductName': self._extract_string(content, 'ProductName'),
                'ProductVersion': self._extract_string(content, 'ProductVersion')
            }
            
            return version_info
            
        except FileNotFoundError:
            self.logger.error(f"版本信息文件不存在: {file_path}")
            raise
        except Exception as e:
            self.logger.error(f"解析版本信息文件时出错: {str(e)}")
            raise ValueError(f"版本信息文件格式错误: {str(e)}")
    
    def save_version_file(self, file_path: str, version_info: Dict[str, str]) -> None:
        """
        保存版本信息到文件。

        Args:
            file_path: 版本信息文件路径
            version_info: 版本信息字典
        """
        try:
            template = self._get_version_template()
            
            # 转换版本号字符串为元组
            filevers = self._version_str_to_tuple(version_info['FileVersion'])
            prodvers = self._version_str_to_tuple(version_info['ProductVersion'])
            
            # 填充模板
            content = template.format(
                filevers=filevers,
                prodvers=prodvers,
                company_name=version_info['CompanyName'],
                file_description=version_info['FileDescription'],
                file_version=version_info['FileVersion'],
                legal_copyright=version_info['LegalCopyright'],
                product_name=version_info['ProductName'],
                product_version=version_info['ProductVersion']
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            self.logger.error(f"保存版本信息文件时出错: {str(e)}")
            raise
    
    def _extract_tuple(self, content: str, key: str) -> Tuple[int, ...]:
        """提取版本号元组"""
        pattern = rf'{key}=\s*\(([\d,\s]+)\)'
        match = re.search(pattern, content)
        if match:
            return tuple(map(int, match.group(1).split(',')))
        return (1, 0, 0, 0)
    
    def _extract_string(self, content: str, key: str) -> str:
        """提取字符串值"""
        pattern = rf"StringStruct\(u'{key}',\s*u'([^']*?)'\)"
        match = re.search(pattern, content)
        return match.group(1) if match else ''
    
    def _version_str_to_tuple(self, version_str: str) -> Tuple[int, ...]:
        """将版本号字符串转换为元组"""
        parts = version_str.split('.')
        while len(parts) < 4:
            parts.append('0')
        return tuple(map(int, parts[:4]))
    
    def _get_version_template(self) -> str:
        """获取版本信息文件模板"""
        return '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    filevers={filevers},
    prodvers={prodvers},
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'080404b0',
        [StringStruct(u'CompanyName', u'{company_name}'),
        StringStruct(u'FileDescription', u'{file_description}'),
        StringStruct(u'FileVersion', u'{file_version}'),
        StringStruct(u'LegalCopyright', u'{legal_copyright}'),
        StringStruct(u'ProductName', u'{product_name}'),
        StringStruct(u'ProductVersion', u'{product_version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [2052, 1200])])
  ]
)
''' 