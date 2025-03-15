import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import json
import os
from tqdm import tqdm
import threading
import tkinter.font as tkFont
import sys

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deepseek 智能翻译")
        self.root.geometry("720x500")
        try:
            # 获取图标文件的路径
            if getattr(sys, 'frozen', False):
                # 如果是打包后的exe
                application_path = sys._MEIPASS
            else:
                # 如果是直接运行的py文件
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(application_path, "translator.ico")
            
            # 设置窗口图标
            self.root.iconbitmap(icon_path)
            # 设置任务栏图标
            self.root.iconbitmap(default=icon_path)
        except Exception as e:
            print(f"设置图标失败: {e}")  # 添加错误信息输出以便调试
            pass
        self.style = ttk.Style()
        
        # 自定义样式
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('微软雅黑', 10))
        self.style.configure('TButton', font=('微软雅黑', 10), padding=6)
        self.style.configure('TEntry', padding=5)
        self.style.configure('Header.TLabel', font=('微软雅黑', 12, 'bold'))
        self.style.configure('Progress.Horizontal.TProgressbar', thickness=20)
        self.style.configure('TLabelframe', background='#f0f0f0', bordercolor='#cccccc', borderwidth=1, relief='solid')
        self.style.configure('TLabelframe.Label', background='#f0f0f0', foreground='#333333', font=('微软雅黑', 10, 'bold'))
        self.style.configure('TCombobox', background='#ffffff', fieldbackground='#ffffff', selectbackground='#0078D4', selectforeground='white')

        # 主布局
        main_frame = ttk.Frame(root)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # API设置区域
        api_frame = ttk.LabelFrame(main_frame, text=" API 密钥设置 ", style='Header.TLabel')
        api_frame.pack(fill='x', pady=10)
        
        ttk.Label(api_frame, text="Deepseek API密钥:").grid(row=0, column=0, padx=5, sticky='w')
        self.api_key = tk.StringVar()
        self.api_entry = ttk.Entry(api_frame, textvariable=self.api_key, show="*", width=40)
        self.api_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # 语言选择区域
        lang_frame = ttk.LabelFrame(main_frame, text=" 语言设置 ", style='Header.TLabel')
        lang_frame.pack(fill='x', pady=10)
        
        ttk.Label(lang_frame, text="源语言:").grid(row=0, column=0, padx=5, sticky='e')
        self.source_lang = ttk.Combobox(lang_frame, values=["中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语"], width=15)
        self.source_lang.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.source_lang.current(0)
        
        ttk.Label(lang_frame, text="目标语言:").grid(row=0, column=2, padx=5, sticky='e')
        self.target_lang = ttk.Combobox(lang_frame, values=["中文", "英语", "日语", "韩语", "法语", "德语", "西班牙语"], width=15)
        self.target_lang.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.target_lang.current(1)

        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text=" 文件操作 ", style='Header.TLabel')
        file_frame.pack(fill='x', pady=10)
        
        self.file_path = tk.StringVar()
        file_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="源文件路径:").grid(row=0, column=0, padx=5, pady=3, sticky='e')
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5, pady=3, sticky='ew')
        ttk.Button(file_frame, text="浏览文件", command=self.browse_file).grid(row=0, column=2, padx=5, sticky='e')

        # 进度显示区域
        progress_frame = ttk.LabelFrame(main_frame, text=" 翻译进度 ", style='Header.TLabel')
        progress_frame.pack(fill='x', pady=10)
        
        self.progress = ttk.Progressbar(progress_frame, style='Progress.Horizontal.TProgressbar', length=600, mode='determinate')
        self.progress.pack(pady=10, padx=10)
        
        self.progress_label = ttk.Label(progress_frame, text="准备就绪", foreground="#0078D4")
        self.progress_label.pack(pady=5)

        # 操作按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)
        
        self.translate_btn = ttk.Button(btn_frame, text="开始翻译", command=self.start_translation, style='Accent.TButton')
        self.translate_btn.pack(side='left', padx=10)

        # 状态显示
        self.status_label = ttk.Label(main_frame, text="当前状态：等待操作", foreground="#666666", background='#f0f0f0')
        self.status_label.pack(pady=5)

        # 配置列权重
        main_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(1, weight=1)

        # 修改按钮样式配置
        self.style.configure('Accent.TButton', 
            font=('微软雅黑', 10, 'bold'),
            padding=6,
            relief='flat',
            borderwidth=0
        )

        self.style.map('Accent.TButton',
            foreground=[('active', '#0078D4'), ('!active', 'black')],
            background=[('active', '#0069b5'), ('!active', '#0078D4')],
            relief=[('pressed', 'flat'), ('!pressed', 'flat')],
            borderwidth=[('active', 0), ('!active', 0)]
        )

        # 统一所有容器的背景色
        main_frame.configure(style='TFrame')
        api_frame.configure(style='TLabelframe')
        lang_frame.configure(style='TLabelframe')
        file_frame.configure(style='TLabelframe')
        progress_frame.configure(style='TLabelframe')
        btn_frame.configure(style='TFrame')

        # 确保所有标签的背景色一致
        for widget in main_frame.winfo_children():
            if isinstance(widget, ttk.Label):
                widget.configure(style='TLabel')

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="选择源文件",
            filetypes=(("文本文件", "*.txt"), ("所有文件", "*.*"))
        )
        if filename:
            self.file_path.set(filename)

    def update_progress(self, value, text):
        self.progress['value'] = value
        self.progress_label['text'] = f"{value}% - {text}"
        self.root.update_idletasks()

    def translate_text(self, text):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key.get()}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": f"请将以下{self.source_lang.get()}翻译成{self.target_lang.get()}：\n{text}"
                    }
                ]
            }
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return text  # 如果翻译失败，返回原文
                
        except Exception as e:
            return text  # 如果发生任何错误，返回原文

    def start_translation(self):
        if not self.api_key.get():
            messagebox.showwarning("警告", "请输入API密钥")
            return
            
        if not self.file_path.get():
            messagebox.showwarning("警告", "请选择源文件")
            return
            
        # 在新线程中执行翻译
        threading.Thread(target=self.translate_file, daemon=True).start()

    def translate_file(self):
        try:
            self.translate_btn['state'] = 'disabled'
            self.status_label['text'] = "正在翻译..."
            
            # 读取源文件
            with open(self.file_path.get(), 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 按段落分割
            paragraphs = content.split('\n\n')
            total = len(paragraphs)
            translated_content = []
            
            # 翻译每个段落
            for i, para in enumerate(paragraphs):
                if para.strip():
                    translated = self.translate_text(para)
                    translated_content.append(translated)
                else:
                    translated_content.append('')
                    
                progress = int((i + 1) / total * 100)
                self.update_progress(progress, f"已翻译 {i + 1}/{total} 段")
            
            # 保存翻译结果
            output_path = os.path.splitext(self.file_path.get())[0] + '_translated.txt'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(translated_content))
            
            self.status_label['text'] = "翻译完成！"
            messagebox.showinfo("成功", f"翻译已完成并保存至：\n{output_path}")
            
        except Exception as e:
            self.status_label['text'] = "就绪"
        
        finally:
            self.translate_btn['state'] = 'normal'
            self.update_progress(0, "0%")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop() 