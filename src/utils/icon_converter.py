from typing import Optional
from PIL import Image
import os
import logging

class IconConverter:
    """
    图像文件转换为ICO格式的工具类。
    支持将常见图像格式（如PNG、JPG等）转换为ICO文件。
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        初始化图标转换器。

        Args:
            logger: 可选的logger对象，用于日志记录
        """
        self.logger = logger or logging.getLogger(__name__)
        
    def convert_to_ico(self, image_path: str, output_path: Optional[str] = None) -> str:
        """
        将图像文件转换为ICO格式。

        Args:
            image_path: 源图像文件路径
            output_path: 输出ICO文件路径，如果未指定则使用源文件名

        Returns:
            str: 生成的ICO文件路径

        Raises:
            ValueError: 当输入文件格式不支持时抛出
            IOError: 当文件操作失败时抛出
        """
        try:
            # 如果未指定输出路径，则使用源文件名
            if not output_path:
                output_path = os.path.splitext(image_path)[0] + '.ico'
                
            # 打开并转换图像
            with Image.open(image_path) as img:
                # 确保图像为RGBA模式
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                    
                # 调整图像大小为标准图标尺寸
                sizes = [(16,16), (32,32), (48,48), (64,64), (128,128)]
                icons = []
                for size in sizes:
                    icon = img.resize(size, Image.Resampling.LANCZOS)
                    icons.append(icon)
                    
                # 保存为ICO文件
                icons[0].save(
                    output_path,
                    format='ICO',
                    sizes=[(icon.width, icon.height) for icon in icons]
                )
                
            self.logger.info(f"成功将 {image_path} 转换为图标文件 {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"转换图标时出错: {str(e)}")
            raise 