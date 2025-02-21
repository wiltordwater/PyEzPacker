from typing import Optional, List
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import os
from pathlib import Path
from PIL import Image
import json

class PackagerApp:
    """
    Python项目打包工具的主GUI应用程序。
    提供用户友好的界面来配置和执行PyInstaller打包操作。
    """
    
    def __init__(self, root: tk.Tk) -> None:
        """
        初始化打包工具的GUI界面。

        Args:
            root: tkinter的根窗口对象
        """
        self.root = root
        self.root.title("Python项目打包工具")
        self.root.geometry("900x700")  # 稍微调大一点窗口
        
        # 设置样式
        self.setup_styles()
        
        self.setup_variables()
        self.create_widgets()
        self.setup_layout()
        
        # 初始化logger
        self.logger = logging.getLogger(__name__)
        
    def setup_styles(self) -> None:
        """设置自定义样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 定义颜色
        primary_color = "#E3F2FD"  # 浅蓝色背景
        secondary_color = "#90CAF9"  # 中等蓝色
        accent_color = "#1976D2"  # 深蓝色
        text_color = "#2C3E50"  # 深色文字
        
        # 配置基本样式
        self.style.configure(
            "TFrame",
            background=primary_color
        )
        
        # 标签框架样式
        self.style.configure(
            "TLabelframe",
            background=primary_color,
            relief="solid",
            borderwidth=1,
            bordercolor=secondary_color
        )
        self.style.configure(
            "TLabelframe.Label",
            background=primary_color,
            foreground=text_color,
            font=('Microsoft YaHei UI', 9, 'bold')  # 使用微软雅黑
        )
        
        # 按钮样式
        self.style.configure(
            "TButton",
            background=secondary_color,
            foreground=text_color,
            borderwidth=0,
            font=('Microsoft YaHei UI', 9),
            padding=5
        )
        self.style.map(
            "TButton",
            background=[('active', accent_color)],
            foreground=[('active', 'white')]
        )
        
        # 主按钮样式（打包按钮）
        self.style.configure(
            "Primary.TButton",
            background=accent_color,
            foreground="white",
            padding=10,
            font=('Microsoft YaHei UI', 10, 'bold')
        )
        self.style.map(
            "Primary.TButton",
            background=[('active', secondary_color)],
            foreground=[('active', text_color)]
        )
        
        # 输入框样式
        self.style.configure(
            "TEntry",
            fieldbackground="white",
            borderwidth=1,
            relief="solid",
            padding=5
        )
        
        # 复选框样式
        self.style.configure(
            "TCheckbutton",
            background=primary_color,
            foreground=text_color,
            font=('Microsoft YaHei UI', 9)
        )
        
        # 标签样式
        self.style.configure(
            "TLabel",
            background=primary_color,
            foreground=text_color,
            font=('Microsoft YaHei UI', 9)
        )
        
        # 设置根窗口背景色
        self.root.configure(bg=primary_color)
        
    def setup_variables(self) -> None:
        """初始化所有需要的变量"""
        self.script_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.onefile = tk.BooleanVar(value=True)
        self.use_venv = tk.BooleanVar(value=False)
        self.venv_path = tk.StringVar()
        self.icon_path = tk.StringVar()
        self.version_file_path = tk.StringVar()
        self.extra_files = []
        
    def create_widgets(self) -> None:
        """创建所有GUI组件"""
        # 使用主按钮样式
        self.pack_button = ttk.Button(
            self.root,
            text="开始打包",
            command=self.start_packaging,
            style="Primary.TButton"
        )
        
    def create_script_frame(self, parent: ttk.Frame) -> None:
        """
        创建主脚本选择框架
        
        Args:
            parent: 父级框架
        """
        frame = ttk.LabelFrame(parent, text="选择主脚本", padding=5)
        ttk.Entry(frame, textvariable=self.script_path).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(frame, text="浏览", command=self.browse_script).pack(side=tk.LEFT)
        frame.pack(fill=tk.X, padx=5, pady=5)
        
    def create_output_frame(self, parent: ttk.Frame) -> None:
        """
        创建输出目录选择框架
        
        Args:
            parent: 父级框架
        """
        frame = ttk.LabelFrame(parent, text="选择输出目录", padding=5)
        ttk.Entry(frame, textvariable=self.output_dir).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(frame, text="浏览", command=self.browse_output).pack(side=tk.LEFT)
        frame.pack(fill=tk.X, padx=5, pady=5)

    def create_options_frame(self, parent: ttk.Frame) -> None:
        """
        创建打包选项框架
        
        Args:
            parent: 父级框架
        """
        frame = ttk.LabelFrame(parent, text="打包选项", padding=5)
        ttk.Checkbutton(
            frame,
            text="生成单文件",
            variable=self.onefile
        ).pack(anchor=tk.W)
        frame.pack(fill=tk.X, padx=5, pady=5)

    def create_venv_frame(self, parent: ttk.Frame) -> None:
        """
        创建虚拟环境配置框架
        
        Args:
            parent: 父级框架
        """
        frame = ttk.LabelFrame(parent, text="虚拟环境配置", padding=5)
        
        ttk.Checkbutton(
            frame,
            text="使用虚拟环境",
            variable=self.use_venv,
            command=self.toggle_venv
        ).pack(anchor=tk.W)
        
        self.venv_frame = ttk.Frame(frame)
        ttk.Entry(
            self.venv_frame,
            textvariable=self.venv_path,
            state='disabled'
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(
            self.venv_frame,
            text="浏览",
            command=self.browse_venv,
            state='disabled'
        ).pack(side=tk.LEFT)
        self.venv_frame.pack(fill=tk.X, expand=True)
        
        frame.pack(fill=tk.X, padx=5, pady=5)

    def create_extra_files_frame(self, parent: ttk.Frame) -> None:
        """创建额外文件选择框架"""
        frame = ttk.LabelFrame(parent, text="额外文件", padding=5)
        
        # 自定义列表框样式
        self.files_listbox = tk.Listbox(
            frame,
            height=6,
            font=('Microsoft YaHei UI', 9),
            bg='white',
            fg='#2C3E50',
            relief='solid',
            borderwidth=1,
            selectmode=tk.SINGLE
        )
        self.files_listbox.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        btn_frame = ttk.Frame(frame)
        ttk.Button(
            btn_frame,
            text="添加文件",
            command=self.add_extra_file
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame,
            text="移除选中",
            command=self.remove_extra_file
        ).pack(side=tk.LEFT, padx=2)
        btn_frame.pack(fill=tk.X)
        
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_icon_frame(self, parent: ttk.Frame) -> None:
        """
        创建图标选择框架
        
        Args:
            parent: 父级框架
        """
        frame = ttk.LabelFrame(parent, text="应用图标", padding=5)
        ttk.Entry(
            frame,
            textvariable=self.icon_path
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(
            frame,
            text="浏览",
            command=self.browse_icon
        ).pack(side=tk.LEFT)
        frame.pack(fill=tk.X, padx=5, pady=5)

    def create_version_frame(self, parent: ttk.Frame) -> None:
        """
        创建版本信息框架
        
        Args:
            parent: 父级框架
        """
        frame = ttk.LabelFrame(parent, text="版本信息", padding=5)
        
        # 版本信息文件路径
        path_frame = ttk.Frame(frame)
        ttk.Entry(
            path_frame,
            textvariable=self.version_file_path
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(
            path_frame,
            text="浏览",
            command=self.browse_version
        ).pack(side=tk.LEFT)
        path_frame.pack(fill=tk.X)
        
        # 版本信息编辑区域
        edit_frame = ttk.LabelFrame(frame, text="编辑版本信息", padding=5)
        
        # 创建版本信息输入框
        self.version_entries = {}
        fields = [
            ('ProductName', '产品名称'),
            ('FileVersion', '文件版本'),
            ('ProductVersion', '产品版本'),
            ('CompanyName', '公司名称'),
            ('FileDescription', '文件描述'),
            ('LegalCopyright', '版权信息')
        ]
        
        for key, label in fields:
            field_frame = ttk.Frame(edit_frame)
            ttk.Label(field_frame, text=label).pack(side=tk.LEFT)
            entry = ttk.Entry(field_frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.version_entries[key] = entry
            field_frame.pack(fill=tk.X, pady=2)
        
        # 保存按钮
        ttk.Button(
            edit_frame,
            text="保存版本信息",
            command=self.save_version_info
        ).pack(pady=5)
        
        edit_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_log_frame(self, parent: ttk.Frame) -> None:
        """创建日志显示区域"""
        frame = ttk.LabelFrame(parent, text="日志输出", padding=5)
        
        # 自定义日志文本框样式
        self.log_text = tk.Text(
            frame,
            height=8,
            wrap=tk.WORD,
            font=('Consolas', 9),  # 使用等宽字体
            bg='white',
            fg='#2C3E50',
            relief='solid',
            borderwidth=1
        )
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_layout(self) -> None:
        """设置主窗口布局，采用两列布局"""
        # 创建左右两个主框架
        left_frame = ttk.Frame(self.root, padding=5)
        right_frame = ttk.Frame(self.root, padding=5)
        
        # 左侧框架
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 主脚本选择
        self.create_script_frame(left_frame)
        # 输出目录选择
        self.create_output_frame(left_frame)
        # 打包选项
        self.create_options_frame(left_frame)
        # 虚拟环境配置
        self.create_venv_frame(left_frame)
        
        # 右侧框架
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # 额外文件选择
        self.create_extra_files_frame(right_frame)
        # 图标选择
        self.create_icon_frame(right_frame)
        # 版本信息
        self.create_version_frame(right_frame)
        
        # 底部框架（跨越左右两列）
        bottom_frame = ttk.Frame(self.root, padding=5)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # 日志显示区域
        self.create_log_frame(bottom_frame)
        # 打包按钮
        self.pack_button.pack(pady=5)

    def toggle_venv(self) -> None:
        """切换虚拟环境选项的状态"""
        state = 'normal' if self.use_venv.get() else 'disabled'
        for widget in self.venv_frame.winfo_children():
            widget.configure(state=state)

    def browse_venv(self) -> None:
        """浏览并选择虚拟环境目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.venv_path.set(directory)

    def add_extra_file(self) -> None:
        """添加额外文件"""
        files = filedialog.askopenfilenames()
        for file in files:
            if file not in self.extra_files:
                self.extra_files.append(file)
                self.files_listbox.insert(tk.END, file)

    def remove_extra_file(self) -> None:
        """移除选中的额外文件"""
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            self.extra_files.pop(index)
            self.files_listbox.delete(index)

    def browse_icon(self) -> None:
        """浏览并选择图标文件"""
        filename = filedialog.askopenfilename(
            filetypes=[
                ("图像文件", "*.png;*.jpg;*.jpeg;*.ico"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.icon_path.set(filename)

    def browse_version(self) -> None:
        """浏览并选择版本信息文件"""
        filename = filedialog.askopenfilename(
            filetypes=[
                ("版本信息文件", "versionmark.txt"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.version_file_path.set(filename)
            self.load_version_info(filename)

    def load_version_info(self, file_path: str) -> None:
        """加载版本信息文件内容"""
        try:
            from utils.version_parser import VersionParser
            parser = VersionParser(self.logger)
            version_info = parser.parse_version_file(file_path)
            
            # 更新输入框
            for key, entry in self.version_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, version_info.get(key, ''))
            
        except Exception as e:
            self.logger.error(f"加载版本信息失败: {str(e)}")
            messagebox.showerror("错误", f"加载版本信息失败: {str(e)}")

    def save_version_info(self) -> None:
        """保存版本信息到文件"""
        file_path = self.version_file_path.get()
        if not file_path:
            # 如果没有选择文件，则在主脚本目录下创建versionmark.txt
            if not self.script_path.get():
                messagebox.showerror("错误", "请先选择主脚本文件！")
                return
            file_path = os.path.join(os.path.dirname(self.script_path.get()), 'versionmark.txt')
            self.version_file_path.set(file_path)
        
        try:
            from utils.version_parser import VersionParser
            parser = VersionParser(self.logger)
            
            # 收集版本信息
            version_info = {
                key: entry.get() or '1.0.0.0' if key in ['FileVersion', 'ProductVersion']  # 为版本号提供默认值
                else entry.get() or '' for key, entry in self.version_entries.items()
            }
            
            # 保存到文件
            parser.save_version_file(file_path, version_info)
            self.logger.info(f"版本信息已保存到: {file_path}")
            messagebox.showinfo("成功", f"版本信息已保存到:\n{file_path}")
            
        except Exception as e:
            self.logger.error(f"保存版本信息失败: {str(e)}")
            messagebox.showerror("错误", f"保存版本信息失败: {str(e)}")

    def browse_script(self) -> None:
        """浏览并选择主脚本文件，并自动扫描相关文件"""
        filename = filedialog.askopenfilename(
            filetypes=[("Python文件", "*.py")]
        )
        if filename:
            self.script_path.set(filename)
            self.scan_project_files(filename)

    def scan_project_files(self, script_path: str) -> None:
        """
        扫描项目文件并自动填充相关选项
        
        Args:
            script_path: 主脚本路径
        """
        try:
            from utils.project_scanner import ProjectScanner
            scanner = ProjectScanner(self.logger)
            result = scanner.scan_project(script_path)
            
            # 设置默认输出目录
            default_output = os.path.join(os.path.dirname(script_path), 'dist')
            self.output_dir.set(default_output)
            
            # 设置虚拟环境
            if result['venv_dir']:
                self.use_venv.set(True)
                self.venv_path.set(result['venv_dir'])
                self.toggle_venv()
                
            # 设置版本信息文件
            if result['version_file']:
                self.version_file_path.set(result['version_file'])
                self.load_version_info(result['version_file'])
                
            # 设置图标
            if result['icon_file']:
                self.icon_path.set(result['icon_file'])
                
            # 添加数据文件
            for file in result['data_files']:
                if file not in self.extra_files:
                    self.extra_files.append(file)
                    self.files_listbox.insert(tk.END, file)
                
            self.logger.info("项目文件扫描完成")
            messagebox.showinfo("扫描完成", "已自动识别项目相关文件")
            
        except Exception as e:
            self.logger.error(f"扫描项目文件时出错: {str(e)}")
            messagebox.showerror("错误", f"扫描项目文件失败: {str(e)}")

    def browse_output(self) -> None:
        """浏览并选择输出目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)
            
    def start_packaging(self) -> None:
        """开始打包流程"""
        if not self.validate_inputs():
            return
        
        try:
            from utils.packager import PyInstaller
            from utils.icon_converter import IconConverter
            
            self.logger.info("开始打包过程...")
            self.pack_button.configure(state='disabled')
            self.pack_button.configure(text="打包中...")
            self.root.update()
            
            # 转换图标（如果需要）
            icon_path = self.icon_path.get()
            if icon_path and not icon_path.endswith('.ico'):
                converter = IconConverter(self.logger)
                icon_path = converter.convert_to_ico(icon_path)
                
            # 准备打包参数
            packager = PyInstaller(self.logger)
            packager.build(
                script_path=self.script_path.get(),
                output_dir=self.output_dir.get(),
                onefile=self.onefile.get(),
                venv_path=self.venv_path.get() if self.use_venv.get() else None,
                icon_path=icon_path,
                extra_files=self.extra_files,
                version_file=self.version_file_path.get() or None
            )
            
            self.logger.info("打包命令已启动，请在新窗口中查看进度")
            messagebox.showinfo("提示", "打包命令已启动，请在新窗口中查看进度")
            
        except Exception as e:
            self.logger.error(f"打包过程中出现错误: {str(e)}")
            messagebox.showerror("错误", f"打包失败: {str(e)}")
        finally:
            self.pack_button.configure(state='normal')
            self.pack_button.configure(text="开始打包")
            
    def validate_inputs(self) -> bool:
        """
        验证用户输入是否有效
        
        Returns:
            bool: 输入是否有效
        """
        if not self.script_path.get():
            messagebox.showerror("错误", "请选择主脚本文件！")
            return False
        if not self.output_dir.get():
            messagebox.showerror("错误", "请选择输出目录！")
            return False
        return True 