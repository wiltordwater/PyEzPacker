import tkinter as tk
import logging
from pathlib import Path
from gui.app import PackagerApp

def setup_logging() -> None:
    """
    配置日志系统
    """
    # 创建logs目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "packager.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main() -> None:
    """
    程序入口点
    """
    # 设置日志
    setup_logging()
    
    # 创建主窗口
    root = tk.Tk()
    app = PackagerApp(root)
    
    # 运行应用
    root.mainloop()

if __name__ == "__main__":
    main() 