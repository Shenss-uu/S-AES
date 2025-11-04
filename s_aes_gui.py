"""
S-AES GUI 界面
提供完整的图形用户界面支持所有S-AES功能
包括：基本加解密、ASCII加解密、多重加密、中间相遇攻击、CBC模式等
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from s_aes import SAES
import random


class SAESGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("S-AES 加密系统")
        self.root.geometry("950x750")
        
        # 设置窗口图标颜色和样式
        self.setup_styles()
        
        # 初始化S-AES实例
        self.saes = SAES()
        
        # 设置UI
        self.setup_ui()
    
    def setup_styles(self):
        """设置全局样式"""
        style = ttk.Style()
        
        # 使用现代主题
        try:
            style.theme_use('clam')
        except:
            pass
        
        # 配置颜色方案
        self.colors = {
            'primary': '#2C3E50',      # 深蓝灰
            'secondary': '#3498DB',    # 亮蓝色
            'success': '#27AE60',      # 绿色
            'danger': '#E74C3C',       # 红色
            'warning': '#F39C12',      # 橙色
            'light': '#ECF0F1',        # 浅灰
            'dark': '#34495E',         # 深灰
            'bg': '#F8F9FA',           # 背景色
            'text': '#2C3E50'          # 文字色
        }
        
        # 配置Frame样式
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('Card.TFrame', background='white', relief='flat')
        
        # 配置Label样式
        style.configure('TLabel', 
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Microsoft YaHei UI', 10))
        style.configure('Title.TLabel',
                       font=('Microsoft YaHei UI', 14, 'bold'),
                       foreground=self.colors['primary'])
        style.configure('Subtitle.TLabel',
                       font=('Microsoft YaHei UI', 11, 'bold'),
                       foreground=self.colors['secondary'])
        style.configure('Info.TLabel',
                       font=('Microsoft YaHei UI', 9),
                       foreground=self.colors['dark'])
        
        # 配置Button样式
        style.configure('Accent.TButton',
                       font=('Microsoft YaHei UI', 10, 'bold'),
                       padding=[20, 10],
                       background=self.colors['secondary'])
        style.configure('Success.TButton',
                       font=('Microsoft YaHei UI', 10),
                       padding=[15, 8])
        style.configure('Danger.TButton',
                       font=('Microsoft YaHei UI', 10),
                       padding=[15, 8])
        
        # 配置Entry样式
        style.configure('TEntry',
                       fieldbackground='white',
                       font=('Consolas', 11),
                       padding=8)

    def setup_ui(self):
        """设置主界面"""
        # 设置背景色
        self.root.configure(bg=self.colors['bg'])
        
        # 创建顶部标题栏
        self.create_header()
        
        # 创建主容器（左右布局）
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True)
        
        # 创建左侧导航栏
        nav_frame = tk.Frame(main_frame, bg='white', width=180)
        nav_frame.pack(side='left', fill='y', padx=(15, 0), pady=10)
        nav_frame.pack_propagate(False)
        
        # 导航栏标题
        nav_title = tk.Label(
            nav_frame,
            text="功能导航",
            font=('Microsoft YaHei UI', 11, 'bold'),
            bg='white',
            fg=self.colors['primary']
        )
        nav_title.pack(pady=(15, 10))
        
        # 分隔线
        separator = tk.Frame(nav_frame, height=2, bg=self.colors['light'])
        separator.pack(fill='x', padx=15, pady=5)
        
        # 创建内容区域
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(side='left', fill='both', expand=True, padx=(10, 15), pady=10)
        
        # 创建各个标签页框架
        self.frames = {}
        frame_names = ['basic', 'ascii', 'double', 'mitm', 'triple', 'cbc']
        
        for name in frame_names:
            frame = tk.Frame(content_frame, bg=self.colors['bg'])
            self.frames[name] = frame
        
        # 设置各个标签页内容
        self.setup_basic_tab(self.frames['basic'])
        self.setup_ascii_tab(self.frames['ascii'])
        self.setup_double_tab(self.frames['double'])
        self.setup_mitm_tab(self.frames['mitm'])
        self.setup_triple_tab(self.frames['triple'])
        self.setup_cbc_tab(self.frames['cbc'])
        
        # 创建导航按钮
        self.nav_buttons = {}
        nav_items = [
            ('basic', '基本加解密'),
            ('ascii', 'ASCII加解密'),
            ('double', '双重加密'),
            ('mitm', '中间相遇攻击'),
            ('triple', '三重加密'),
            ('cbc', 'CBC模式')
        ]
        
        for name, text in nav_items:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=('Microsoft YaHei UI', 10),
                bg='white',
                fg=self.colors['text'],
                relief='flat',
                bd=0,
                padx=20,
                pady=12,
                anchor='center',
                cursor='hand2',
                command=lambda n=name: self.show_frame(n)
            )
            btn.pack(fill='x', padx=5, pady=2)
            self.nav_buttons[name] = btn
        
        # 默认显示第一个页面
        self.current_frame = None
        self.show_frame('basic')
    
    def show_frame(self, frame_name):
        """切换显示的框架"""
        # 隐藏当前框架
        if self.current_frame:
            self.frames[self.current_frame].pack_forget()
            # 重置之前按钮的样式
            self.nav_buttons[self.current_frame].config(
                bg='white',
                fg=self.colors['text'],
                font=('Microsoft YaHei UI', 10)
            )
        
        # 显示新框架
        self.frames[frame_name].pack(fill='both', expand=True)
        self.current_frame = frame_name
        
        # 高亮当前按钮
        self.nav_buttons[frame_name].config(
            bg=self.colors['secondary'],
            fg='white',
            font=('Microsoft YaHei UI', 10, 'bold')
        )
    
    def create_header(self):
        """创建顶部标题栏"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # 主标题
        title_label = tk.Label(
            header_frame,
            text="S-AES 加密系统",
            font=('Microsoft YaHei UI', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(pady=(12, 3))
        
        # 副标题
        subtitle_label = tk.Label(
            header_frame,
            text="Simplified Advanced Encryption Standard",
            font=('Microsoft YaHei UI', 9),
            bg=self.colors['primary'],
            fg=self.colors['light']
        )
        subtitle_label.pack(pady=(0, 12))
    
    def create_card_frame(self, parent):
        """创建卡片式框架"""
        card = tk.Frame(parent, bg='white', relief='flat', bd=1)
        card.configure(highlightbackground=self.colors['light'], highlightthickness=1)
        return card

    # ==================== 第1关：基本加解密 ====================

    def setup_basic_tab(self, frame):
        """设置基本加解密标签页"""
        frame.configure(bg=self.colors['bg'])
        
        # 主容器
        main_container = tk.Frame(frame, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题区域
        title_frame = self.create_card_frame(main_container)
        title_frame.pack(fill='x', pady=(0, 12))
        
        title_label = tk.Label(
            title_frame,
            text="基本加解密",
            font=('Microsoft YaHei UI', 14, 'bold'),
            bg='white',
            fg=self.colors['primary']
        )
        title_label.pack(pady=(12, 3))
        
        subtitle_label = tk.Label(
            title_frame,
            text="16位数据块  •  16位密钥  •  支持交叉测试",
            font=('Microsoft YaHei UI', 9),
            bg='white',
            fg=self.colors['dark']
        )
        subtitle_label.pack(pady=(0, 12))
        
        # 输入区域
        input_frame = self.create_card_frame(main_container)
        input_frame.pack(fill='x', pady=(0, 15))
        
        input_inner = tk.Frame(input_frame, bg='white')
        input_inner.pack(fill='x', padx=30, pady=20)
        
        # 明文输入
        plaintext_label = tk.Label(
            input_inner,
            text="明文 (16进制):",
            font=('Microsoft YaHei UI', 11),
            bg='white',
            fg=self.colors['text']
        )
        plaintext_label.grid(row=0, column=0, sticky='w', pady=8)
        
        self.basic_plaintext = tk.Entry(
            input_inner,
            font=('Consolas', 12),
            width=25,
            relief='solid',
            bd=1
        )
        self.basic_plaintext.grid(row=0, column=1, padx=15, pady=8)
        
        plaintext_hint = tk.Label(
            input_inner,
            text="例: 1234",
            font=('Microsoft YaHei UI', 9),
            bg='white',
            fg=self.colors['dark']
        )
        plaintext_hint.grid(row=0, column=2, sticky='w', padx=5)
        
        # 密钥输入
        key_label = tk.Label(
            input_inner,
            text="密钥 (16进制):",
            font=('Microsoft YaHei UI', 11),
            bg='white',
            fg=self.colors['text']
        )
        key_label.grid(row=1, column=0, sticky='w', pady=8)
        
        self.basic_key = tk.Entry(
            input_inner,
            font=('Consolas', 12),
            width=25,
            relief='solid',
            bd=1
        )
        self.basic_key.grid(row=1, column=1, padx=15, pady=8)
        
        key_hint = tk.Label(
            input_inner,
            text="例: 2D55",
            font=('Microsoft YaHei UI', 9),
            bg='white',
            fg=self.colors['dark']
        )
        key_hint.grid(row=1, column=2, sticky='w', padx=5)
        
        # 密文输入
        cipher_label = tk.Label(
            input_inner,
            text="密文 (16进制):",
            font=('Microsoft YaHei UI', 11),
            bg='white',
            fg=self.colors['text']
        )
        cipher_label.grid(row=2, column=0, sticky='w', pady=8)
        
        self.basic_ciphertext = tk.Entry(
            input_inner,
            font=('Consolas', 12),
            width=25,
            relief='solid',
            bd=1
        )
        self.basic_ciphertext.grid(row=2, column=1, padx=15, pady=8)
        
        cipher_hint = tk.Label(
            input_inner,
            text="加密后自动填充",
            font=('Microsoft YaHei UI', 9),
            bg='white',
            fg=self.colors['dark']
        )
        cipher_hint.grid(row=2, column=2, sticky='w', padx=5)
        
        # 按钮区域
        button_frame = tk.Frame(input_inner, bg='white')
        button_frame.grid(row=3, column=0, columnspan=3, pady=18)
        
        encrypt_btn = tk.Button(
            button_frame,
            text="加 密",
            font=('Microsoft YaHei UI', 10, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief='flat',
            padx=35,
            pady=8,
            cursor='hand2',
            command=self.basic_encrypt,
            activebackground='#2980B9',
            activeforeground='white'
        )
        encrypt_btn.pack(side='left', padx=5)
        
        decrypt_btn = tk.Button(
            button_frame,
            text="解 密",
            font=('Microsoft YaHei UI', 10, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief='flat',
            padx=35,
            pady=8,
            cursor='hand2',
            command=self.basic_decrypt,
            activebackground='#229954',
            activeforeground='white'
        )
        decrypt_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="清 空",
            font=('Microsoft YaHei UI', 10),
            bg=self.colors['light'],
            fg=self.colors['text'],
            relief='flat',
            padx=30,
            pady=8,
            cursor='hand2',
            command=self.basic_clear,
            activebackground='#BDC3C7',
            activeforeground=self.colors['text']
        )
        clear_btn.pack(side='left', padx=5)
        
        # 结果显示区域
        result_frame = self.create_card_frame(main_container)
        result_frame.pack(fill='both', expand=True)
        
        result_title = tk.Label(
            result_frame,
            text="运算结果",
            font=('Microsoft YaHei UI', 11, 'bold'),
            bg='white',
            fg=self.colors['primary']
        )
        result_title.pack(pady=(12, 8), padx=20, anchor='w')
        
        self.basic_result = scrolledtext.ScrolledText(
            result_frame,
            height=10,
            width=80,
            font=('Consolas', 10),
            relief='flat',
            bg='#F8F9FA',
            fg=self.colors['text'],
            wrap='word'
        )
        self.basic_result.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def basic_encrypt(self):
        """基本加密"""
        try:
            plaintext_str = self.basic_plaintext.get().strip()
            key_str = self.basic_key.get().strip()
            
            if not plaintext_str or not key_str:
                messagebox.showwarning("警告", "请输入明文和密钥")
                return
            
            plaintext = int(plaintext_str, 16)
            key = int(key_str, 16)
            
            # 验证范围
            if plaintext > 0xFFFF or key > 0xFFFF:
                messagebox.showerror("错误", "明文和密钥必须是16位（0000-FFFF）")
                return

            ciphertext = self.saes.encrypt(plaintext, key)
            
            self.basic_ciphertext.delete(0, tk.END)
            self.basic_ciphertext.insert(0, f"{ciphertext:04X}")
            
            result = (f"{'='*65}\n"
                     f"  加密成功\n"
                     f"{'='*65}\n\n"
                     f"明文 (Plaintext):\n"
                     f"  十六进制: {plaintext:04X}\n"
                     f"  十进制:   {plaintext}\n"
                     f"  二进制:   {plaintext:016b}\n\n"
                     f"密钥 (Key):\n"
                     f"  十六进制: {key:04X}\n"
                     f"  十进制:   {key}\n\n"
                     f"密文 (Ciphertext):\n"
                     f"  十六进制: {ciphertext:04X}\n"
                     f"  十进制:   {ciphertext}\n"
                     f"  二进制:   {ciphertext:016b}\n\n"
                     f"{'='*65}\n")
            
            self.basic_result.delete(1.0, tk.END)
            self.basic_result.insert(tk.END, result)

        except ValueError:
            messagebox.showerror("错误", "请输入有效的16进制数字")

    def basic_decrypt(self):
        """基本解密"""
        try:
            ciphertext_str = self.basic_ciphertext.get().strip()
            key_str = self.basic_key.get().strip()
            
            if not ciphertext_str or not key_str:
                messagebox.showwarning("警告", "请输入密文和密钥")
                return
            
            ciphertext = int(ciphertext_str, 16)
            key = int(key_str, 16)
            
            if ciphertext > 0xFFFF or key > 0xFFFF:
                messagebox.showerror("错误", "密文和密钥必须是16位（0000-FFFF）")
                return

            plaintext = self.saes.decrypt(ciphertext, key)
            
            self.basic_plaintext.delete(0, tk.END)
            self.basic_plaintext.insert(0, f"{plaintext:04X}")
            
            result = (f"{'='*65}\n"
                     f"  解密成功\n"
                     f"{'='*65}\n\n"
                     f"密文 (Ciphertext):\n"
                     f"  十六进制: {ciphertext:04X}\n"
                     f"  十进制:   {ciphertext}\n"
                     f"  二进制:   {ciphertext:016b}\n\n"
                     f"密钥 (Key):\n"
                     f"  十六进制: {key:04X}\n"
                     f"  十进制:   {key}\n\n"
                     f"明文 (Plaintext):\n"
                     f"  十六进制: {plaintext:04X}\n"
                     f"  十进制:   {plaintext}\n"
                     f"  二进制:   {plaintext:016b}\n\n"
                     f"{'='*65}\n")
            
            self.basic_result.delete(1.0, tk.END)
            self.basic_result.insert(tk.END, result)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的16进制数字")
    
    def basic_clear(self):
        """清空基本加解密界面"""
        self.basic_plaintext.delete(0, tk.END)
        self.basic_key.delete(0, tk.END)
        self.basic_ciphertext.delete(0, tk.END)
        self.basic_result.delete(1.0, tk.END)
    
    # ==================== 第3关：ASCII加解密 ====================
    
    def setup_ascii_tab(self, frame):
        """设置ASCII加解密标签页"""
        title = ttk.Label(frame, text="ASCII 字符串加解密 (2字节分组)", 
                         font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # 明文输入
        ttk.Label(frame, text="明文 (字符串):").grid(row=1, column=0, padx=5, pady=5, sticky='ne')
        self.ascii_plaintext = scrolledtext.ScrolledText(frame, height=3, width=50)
        self.ascii_plaintext.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        # 密钥输入
        ttk.Label(frame, text="密钥 (16进制):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.ascii_key = ttk.Entry(frame, width=20)
        self.ascii_key.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # 密文输入
        ttk.Label(frame, text="密文 (16进制块):").grid(row=3, column=0, padx=5, pady=5, sticky='ne')
        self.ascii_ciphertext = scrolledtext.ScrolledText(frame, height=3, width=50)
        self.ascii_ciphertext.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        
        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="加密", command=self.ascii_encrypt).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="解密", command=self.ascii_decrypt).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="清空", command=self.ascii_clear).pack(side='left', padx=5)
        
        # 结果显示
        ttk.Label(frame, text="结果:").grid(row=5, column=0, padx=5, pady=5, sticky='ne')
        self.ascii_result = scrolledtext.ScrolledText(frame, height=12, width=70)
        self.ascii_result.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        
        # 说明
        info = ("说明：\n"
               "1. 输入任意ASCII/UTF-8字符串作为明文\n"
               "2. 字符串将按2字节（16位）分组加密\n"
               "3. 密文显示为16进制块列表")
        ttk.Label(frame, text=info, justify='left', foreground='blue').grid(
            row=6, column=0, columnspan=3, padx=10, pady=10)
    
    def ascii_encrypt(self):
        """ASCII加密"""
        try:
            plaintext_str = self.ascii_plaintext.get(1.0, tk.END).strip()
            key_str = self.ascii_key.get().strip()
            
            if not plaintext_str or not key_str:
                messagebox.showwarning("警告", "请输入明文和密钥")
                return
            
            key = int(key_str, 16)
            
            if key > 0xFFFF:
                messagebox.showerror("错误", "密钥必须是16位（0000-FFFF）")
                return
            
            # 加密
            ciphertext_blocks = self.saes.encrypt_ascii(plaintext_str, key)
            
            # 显示密文块
            cipher_str = ' '.join([f"{block:04X}" for block in ciphertext_blocks])
            self.ascii_ciphertext.delete(1.0, tk.END)
            self.ascii_ciphertext.insert(1.0, cipher_str)
            
            # 显示结果
            result = (f"=== 加密成功 ===\n"
                     f"明文: {plaintext_str}\n"
                     f"明文长度: {len(plaintext_str)} 字符\n"
                     f"密钥: {key:04X}\n"
                     f"密文块数: {len(ciphertext_blocks)}\n"
                     f"密文 (16进制): {cipher_str}\n")
            
            self.ascii_result.delete(1.0, tk.END)
            self.ascii_result.insert(tk.END, result)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的16进制密钥")
    
    def ascii_decrypt(self):
        """ASCII解密"""
        try:
            cipher_str = self.ascii_ciphertext.get(1.0, tk.END).strip()
            key_str = self.ascii_key.get().strip()
            
            if not cipher_str or not key_str:
                messagebox.showwarning("警告", "请输入密文和密钥")
                return
            
            key = int(key_str, 16)
            
            if key > 0xFFFF:
                messagebox.showerror("错误", "密钥必须是16位（0000-FFFF）")
                return
            
            # 解析密文块
            cipher_parts = cipher_str.split()
            ciphertext_blocks = [int(block, 16) for block in cipher_parts]
            
            # 解密
            plaintext_str = self.saes.decrypt_ascii(ciphertext_blocks, key)
            
            # 显示明文
            self.ascii_plaintext.delete(1.0, tk.END)
            self.ascii_plaintext.insert(1.0, plaintext_str)
            
            # 显示结果
            result = (f"=== 解密成功 ===\n"
                     f"密文块数: {len(ciphertext_blocks)}\n"
                     f"密钥: {key:04X}\n"
                     f"明文: {plaintext_str}\n"
                     f"明文长度: {len(plaintext_str)} 字符\n")
            
            self.ascii_result.delete(1.0, tk.END)
            self.ascii_result.insert(tk.END, result)
            
        except ValueError as e:
            messagebox.showerror("错误", f"请输入有效的16进制密文块: {str(e)}")
    
    def ascii_clear(self):
        """清空ASCII界面"""
        self.ascii_plaintext.delete(1.0, tk.END)
        self.ascii_key.delete(0, tk.END)
        self.ascii_ciphertext.delete(1.0, tk.END)
        self.ascii_result.delete(1.0, tk.END)
    
    # ==================== 第4.1关：双重加密 ====================
    
    def setup_double_tab(self, frame):
        """设置双重加密标签页"""
        title = ttk.Label(frame, text="双重加密 (32位密钥 = K1 + K2)", 
                         font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # 明文输入
        ttk.Label(frame, text="明文 (16进制):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.double_plaintext = ttk.Entry(frame, width=20)
        self.double_plaintext.grid(row=1, column=1, padx=5, pady=5)
        
        # 密钥1输入
        ttk.Label(frame, text="密钥K1 (16进制):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.double_key1 = ttk.Entry(frame, width=20)
        self.double_key1.grid(row=2, column=1, padx=5, pady=5)
        
        # 密钥2输入
        ttk.Label(frame, text="密钥K2 (16进制):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.double_key2 = ttk.Entry(frame, width=20)
        self.double_key2.grid(row=3, column=1, padx=5, pady=5)
        
        # 密文输入
        ttk.Label(frame, text="密文 (16进制):").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.double_ciphertext = ttk.Entry(frame, width=20)
        self.double_ciphertext.grid(row=4, column=1, padx=5, pady=5)
        
        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="加密", command=self.double_encrypt).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="解密", command=self.double_decrypt).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="清空", command=self.double_clear).pack(side='left', padx=5)
        
        # 结果显示
        ttk.Label(frame, text="结果:").grid(row=6, column=0, padx=5, pady=5, sticky='ne')
        self.double_result = scrolledtext.ScrolledText(frame, height=12, width=70)
        self.double_result.grid(row=6, column=1, columnspan=2, padx=5, pady=5)
        
        # 说明
        info = ("说明：\n"
               "1. 双重加密使用两个16位密钥: C = E_K2(E_K1(P))\n"
               "2. 双重解密: P = D_K1(D_K2(C))\n"
               "3. 总密钥长度为32位，提供更强的安全性")
        ttk.Label(frame, text=info, justify='left', foreground='blue').grid(
            row=7, column=0, columnspan=3, padx=10, pady=10)
    
    def double_encrypt(self):
        """双重加密"""
        try:
            plaintext_str = self.double_plaintext.get().strip()
            key1_str = self.double_key1.get().strip()
            key2_str = self.double_key2.get().strip()
            
            if not plaintext_str or not key1_str or not key2_str:
                messagebox.showwarning("警告", "请输入明文和两个密钥")
                return
            
            plaintext = int(plaintext_str, 16)
            key1 = int(key1_str, 16)
            key2 = int(key2_str, 16)
            
            if plaintext > 0xFFFF or key1 > 0xFFFF or key2 > 0xFFFF:
                messagebox.showerror("错误", "所有值必须是16位（0000-FFFF）")
                return
            
            ciphertext = self.saes.double_encrypt(plaintext, key1, key2)
            
            self.double_ciphertext.delete(0, tk.END)
            self.double_ciphertext.insert(0, f"{ciphertext:04X}")
            
            result = (f"=== 双重加密成功 ===\n"
                     f"明文 P: {plaintext:04X}\n"
                     f"密钥 K1: {key1:04X}\n"
                     f"密钥 K2: {key2:04X}\n"
                     f"32位组合密钥: {key1:04X}{key2:04X}\n"
                     f"中间值 E_K1(P): {self.saes.encrypt(plaintext, key1):04X}\n"
                     f"密文 C = E_K2(E_K1(P)): {ciphertext:04X}\n")
            
            self.double_result.delete(1.0, tk.END)
            self.double_result.insert(tk.END, result)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的16进制数字")
    
    def double_decrypt(self):
        """双重解密"""
        try:
            ciphertext_str = self.double_ciphertext.get().strip()
            key1_str = self.double_key1.get().strip()
            key2_str = self.double_key2.get().strip()
            
            if not ciphertext_str or not key1_str or not key2_str:
                messagebox.showwarning("警告", "请输入密文和两个密钥")
                return
            
            ciphertext = int(ciphertext_str, 16)
            key1 = int(key1_str, 16)
            key2 = int(key2_str, 16)
            
            if ciphertext > 0xFFFF or key1 > 0xFFFF or key2 > 0xFFFF:
                messagebox.showerror("错误", "所有值必须是16位（0000-FFFF）")
                return
            
            plaintext = self.saes.double_decrypt(ciphertext, key1, key2)
            
            self.double_plaintext.delete(0, tk.END)
            self.double_plaintext.insert(0, f"{plaintext:04X}")
            
            result = (f"=== 双重解密成功 ===\n"
                     f"密文 C: {ciphertext:04X}\n"
                     f"密钥 K1: {key1:04X}\n"
                     f"密钥 K2: {key2:04X}\n"
                     f"32位组合密钥: {key1:04X}{key2:04X}\n"
                     f"中间值 D_K2(C): {self.saes.decrypt(ciphertext, key2):04X}\n"
                     f"明文 P = D_K1(D_K2(C)): {plaintext:04X}\n")
            
            self.double_result.delete(1.0, tk.END)
            self.double_result.insert(tk.END, result)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的16进制数字")
    
    def double_clear(self):
        """清空双重加密界面"""
        self.double_plaintext.delete(0, tk.END)
        self.double_key1.delete(0, tk.END)
        self.double_key2.delete(0, tk.END)
        self.double_ciphertext.delete(0, tk.END)
        self.double_result.delete(1.0, tk.END)
    
    # ==================== 第4.2关：中间相遇攻击 ====================
    
    def setup_mitm_tab(self, frame):
        """设置中间相遇攻击标签页"""
        title = ttk.Label(frame, text="中间相遇攻击 (破解双重加密)", 
                         font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # 明文输入
        ttk.Label(frame, text="已知明文 (16进制):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.mitm_plaintext = ttk.Entry(frame, width=20)
        self.mitm_plaintext.grid(row=1, column=1, padx=5, pady=5)
        
        # 密文输入
        ttk.Label(frame, text="已知密文 (16进制):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.mitm_ciphertext = ttk.Entry(frame, width=20)
        self.mitm_ciphertext.grid(row=2, column=1, padx=5, pady=5)
        
        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="开始攻击", command=self.mitm_attack).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="清空", command=self.mitm_clear).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="生成测试数据", command=self.mitm_generate).pack(side='left', padx=5)
        
        # 进度条
        ttk.Label(frame, text="攻击进度:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.mitm_progress = ttk.Progressbar(frame, length=400, mode='determinate')
        self.mitm_progress.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
        
        # 结果显示
        ttk.Label(frame, text="攻击结果:").grid(row=5, column=0, padx=5, pady=5, sticky='ne')
        self.mitm_result = scrolledtext.ScrolledText(frame, height=15, width=70)
        self.mitm_result.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        
        # 说明
        info = ("说明：\n"
               "1. 输入已知的明文-密文对\n"
               "2. 程序将尝试找到所有可能的密钥对(K1, K2)\n"
               "3. 警告：这将遍历所有可能的密钥组合，需要较长时间\n"
               "4. 建议先点击'生成测试数据'创建测试用例")
        ttk.Label(frame, text=info, justify='left', foreground='blue').grid(
            row=6, column=0, columnspan=3, padx=10, pady=10)
    
    def mitm_generate(self):
        """生成测试数据"""
        # 随机生成明文和密钥
        plaintext = random.randint(0, 0xFFFF)
        key1 = random.randint(0, 0xFFFF)
        key2 = random.randint(0, 0xFFFF)
        
        # 进行双重加密
        ciphertext = self.saes.double_encrypt(plaintext, key1, key2)
        
        # 填充数据
        self.mitm_plaintext.delete(0, tk.END)
        self.mitm_plaintext.insert(0, f"{plaintext:04X}")
        self.mitm_ciphertext.delete(0, tk.END)
        self.mitm_ciphertext.insert(0, f"{ciphertext:04X}")
        
        # 显示正确密钥
        result = (f"=== 测试数据已生成 ===\n"
                 f"明文: {plaintext:04X}\n"
                 f"正确密钥 K1: {key1:04X}\n"
                 f"正确密钥 K2: {key2:04X}\n"
                 f"密文: {ciphertext:04X}\n"
                 f"\n现在点击'开始攻击'尝试破解密钥\n")
        
        self.mitm_result.delete(1.0, tk.END)
        self.mitm_result.insert(tk.END, result)
    
    def mitm_attack(self):
        """执行中间相遇攻击"""
        try:
            plaintext_str = self.mitm_plaintext.get().strip()
            ciphertext_str = self.mitm_ciphertext.get().strip()
            
            if not plaintext_str or not ciphertext_str:
                messagebox.showwarning("警告", "请输入明文和密文")
                return
            
            plaintext = int(plaintext_str, 16)
            ciphertext = int(ciphertext_str, 16)
            
            if plaintext > 0xFFFF or ciphertext > 0xFFFF:
                messagebox.showerror("错误", "明文和密文必须是16位（0000-FFFF）")
                return
            
            # 显示开始信息
            self.mitm_result.delete(1.0, tk.END)
            self.mitm_result.insert(tk.END, "正在执行中间相遇攻击...\n")
            self.mitm_result.insert(tk.END, "这可能需要几秒钟时间，请耐心等待...\n\n")
            self.root.update()
            
            # 执行攻击
            self.mitm_progress['value'] = 0
            possible_keys = self.saes.meet_in_middle_attack(plaintext, ciphertext)
            self.mitm_progress['value'] = 100
            
            # 显示结果
            result = f"\n=== 攻击完成 ===\n"
            result += f"找到 {len(possible_keys)} 个可能的密钥对\n\n"
            
            if possible_keys:
                result += "可能的密钥对 (K1, K2):\n"
                for i, (k1, k2) in enumerate(possible_keys[:30]):  # 只显示前30个
                    result += f"{i+1}. K1={k1:04X}, K2={k2:04X}\n"
                    # 验证密钥
                    test_cipher = self.saes.double_encrypt(plaintext, k1, k2)
                    if test_cipher == ciphertext:
                        result += f"   ✓ 验证通过\n"
                
                if len(possible_keys) > 30:
                    result += f"\n... 还有 {len(possible_keys) - 30} 个密钥对未显示\n"
            else:
                result += "未找到有效的密钥对\n"
            
            self.mitm_result.delete(1.0, tk.END)
            self.mitm_result.insert(tk.END, result)

        except ValueError:
            messagebox.showerror("错误", "请输入有效的16进制数字")

    def mitm_clear(self):
        """清空中间相遇攻击界面"""
        self.mitm_plaintext.delete(0, tk.END)
        self.mitm_ciphertext.delete(0, tk.END)
        self.mitm_result.delete(1.0, tk.END)
        self.mitm_progress['value'] = 0
    
    # ==================== 第4.3关：三重加密 ====================
    
    def setup_triple_tab(self, frame):
        """设置三重加密标签页"""
        title = ttk.Label(frame, text="三重加密 (支持32位和48位密钥)", 
                         font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # 加密模式选择
        ttk.Label(frame, text="加密模式:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.triple_mode = ttk.Combobox(frame, values=["32位密钥 (K1+K2)", "48位密钥 (K1+K2+K3)"], 
                                        state='readonly', width=25)
        self.triple_mode.current(0)
        self.triple_mode.grid(row=1, column=1, padx=5, pady=5)
        self.triple_mode.bind('<<ComboboxSelected>>', self.triple_mode_changed)
        
        # 明文输入
        ttk.Label(frame, text="明文 (16进制):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.triple_plaintext = ttk.Entry(frame, width=20)
        self.triple_plaintext.grid(row=2, column=1, padx=5, pady=5)
        
        # 密钥输入
        ttk.Label(frame, text="密钥K1 (16进制):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.triple_key1 = ttk.Entry(frame, width=20)
        self.triple_key1.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="密钥K2 (16进制):").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.triple_key2 = ttk.Entry(frame, width=20)
        self.triple_key2.grid(row=4, column=1, padx=5, pady=5)
        
        self.triple_key3_label = ttk.Label(frame, text="密钥K3 (16进制):")
        self.triple_key3_label.grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.triple_key3 = ttk.Entry(frame, width=20, state='disabled')
        self.triple_key3.grid(row=5, column=1, padx=5, pady=5)
        
        # 密文输入
        ttk.Label(frame, text="密文 (16进制):").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        self.triple_ciphertext = ttk.Entry(frame, width=20)
        self.triple_ciphertext.grid(row=6, column=1, padx=5, pady=5)
        
        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=7, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="加密", command=self.triple_encrypt).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="解密", command=self.triple_decrypt).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="清空", command=self.triple_clear).pack(side='left', padx=5)
        
        # 结果显示
        ttk.Label(frame, text="结果:").grid(row=8, column=0, padx=5, pady=5, sticky='ne')
        self.triple_result = scrolledtext.ScrolledText(frame, height=10, width=70)
        self.triple_result.grid(row=8, column=1, columnspan=2, padx=5, pady=5)
        
        # 说明
        info = ("说明：\n"
               "1. 32位模式: C = E_K1(D_K2(E_K1(P))) (EDE模式)\n"
               "2. 48位模式: C = E_K3(D_K2(E_K1(P))) (使用三个独立密钥)\n"
                "3. 选择32位模式时密钥K3不可输入")
        ttk.Label(frame, text=info, justify='left', foreground='blue').grid(
            row=9, column=0, columnspan=3, padx=10, pady=10)
    
    def triple_mode_changed(self, event):
        """三重加密模式改变"""
        if self.triple_mode.current() == 0:  # 32位模式
            self.triple_key3.config(state='disabled')
        else:  # 48位模式
            self.triple_key3.config(state='normal')
    
    def triple_encrypt(self):
        """三重加密"""
        try:
            plaintext_str = self.triple_plaintext.get().strip()
            key1_str = self.triple_key1.get().strip()
            key2_str = self.triple_key2.get().strip()
            
            if not plaintext_str or not key1_str or not key2_str:
                messagebox.showwarning("警告", "请输入明文和密钥")
                return
            
            plaintext = int(plaintext_str, 16)
            key1 = int(key1_str, 16)
            key2 = int(key2_str, 16)
            
            if plaintext > 0xFFFF or key1 > 0xFFFF or key2 > 0xFFFF:
                messagebox.showerror("错误", "所有值必须是16位（0000-FFFF）")
                return
            
            if self.triple_mode.current() == 0:  # 32位模式
                ciphertext = self.saes.triple_encrypt_32bit(plaintext, key1, key2)
                temp1 = self.saes.encrypt(plaintext, key1)
                temp2 = self.saes.decrypt(temp1, key2)
                
                result = (f"=== 三重加密成功 (32位模式) ===\n"
                         f"明文 P: {plaintext:04X}\n"
                         f"密钥 K1: {key1:04X}\n"
                         f"密钥 K2: {key2:04X}\n"
                         f"中间值1 E_K1(P): {temp1:04X}\n"
                         f"中间值2 D_K2(E_K1(P)): {temp2:04X}\n"
                         f"密文 C = E_K1(D_K2(E_K1(P))): {ciphertext:04X}\n")
            else:  # 48位模式
                key3_str = self.triple_key3.get().strip()
                if not key3_str:
                    messagebox.showwarning("警告", "48位模式需要输入K3")
                    return
                key3 = int(key3_str, 16)
                if key3 > 0xFFFF:
                    messagebox.showerror("错误", "K3必须是16位（0000-FFFF）")
                    return
                
                ciphertext = self.saes.triple_encrypt_48bit(plaintext, key1, key2, key3)
                temp1 = self.saes.encrypt(plaintext, key1)
                temp2 = self.saes.decrypt(temp1, key2)
                
                result = (f"=== 三重加密成功 (48位模式) ===\n"
                         f"明文 P: {plaintext:04X}\n"
                         f"密钥 K1: {key1:04X}\n"
                         f"密钥 K2: {key2:04X}\n"
                         f"密钥 K3: {key3:04X}\n"
                         f"中间值1 E_K1(P): {temp1:04X}\n"
                         f"中间值2 D_K2(E_K1(P)): {temp2:04X}\n"
                         f"密文 C = E_K3(D_K2(E_K1(P))): {ciphertext:04X}\n")
            
            self.triple_ciphertext.delete(0, tk.END)
            self.triple_ciphertext.insert(0, f"{ciphertext:04X}")
            
            self.triple_result.delete(1.0, tk.END)
            self.triple_result.insert(tk.END, result)

        except ValueError:
            messagebox.showerror("错误", "请输入有效的16进制数字")

    def triple_decrypt(self):
        """三重解密"""
        try:
            ciphertext_str = self.triple_ciphertext.get().strip()
            key1_str = self.triple_key1.get().strip()
            key2_str = self.triple_key2.get().strip()
            
            if not ciphertext_str or not key1_str or not key2_str:
                messagebox.showwarning("警告", "请输入密文和密钥")
                return
            
            ciphertext = int(ciphertext_str, 16)
            key1 = int(key1_str, 16)
            key2 = int(key2_str, 16)
            
            if ciphertext > 0xFFFF or key1 > 0xFFFF or key2 > 0xFFFF:
                messagebox.showerror("错误", "所有值必须是16位（0000-FFFF）")
                return
            
            if self.triple_mode.current() == 0:  # 32位模式
                plaintext = self.saes.triple_decrypt_32bit(ciphertext, key1, key2)
                
                result = (f"=== 三重解密成功 (32位模式) ===\n"
                         f"密文 C: {ciphertext:04X}\n"
                         f"密钥 K1: {key1:04X}\n"
                         f"密钥 K2: {key2:04X}\n"
                         f"明文 P = D_K1(E_K2(D_K1(C))): {plaintext:04X}\n")
            else:  # 48位模式
                key3_str = self.triple_key3.get().strip()
                if not key3_str:
                    messagebox.showwarning("警告", "48位模式需要输入K3")
                    return
                key3 = int(key3_str, 16)
                if key3 > 0xFFFF:
                    messagebox.showerror("错误", "K3必须是16位（0000-FFFF）")
                    return
                
                plaintext = self.saes.triple_decrypt_48bit(ciphertext, key1, key2, key3)
                
                result = (f"=== 三重解密成功 (48位模式) ===\n"
                         f"密文 C: {ciphertext:04X}\n"
                         f"密钥 K1: {key1:04X}\n"
                         f"密钥 K2: {key2:04X}\n"
                         f"密钥 K3: {key3:04X}\n"
                         f"明文 P = D_K1(E_K2(D_K3(C))): {plaintext:04X}\n")
            
            self.triple_plaintext.delete(0, tk.END)
            self.triple_plaintext.insert(0, f"{plaintext:04X}")
            
            self.triple_result.delete(1.0, tk.END)
            self.triple_result.insert(tk.END, result)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的16进制数字")
    
    def triple_clear(self):
        """清空三重加密界面"""
        self.triple_plaintext.delete(0, tk.END)
        self.triple_key1.delete(0, tk.END)
        self.triple_key2.delete(0, tk.END)
        self.triple_key3.delete(0, tk.END)
        self.triple_ciphertext.delete(0, tk.END)
        self.triple_result.delete(1.0, tk.END)
    
    # ==================== 第5关：CBC模式 ====================

    def setup_cbc_tab(self, frame):
        """设置CBC模式标签页"""
        title = ttk.Label(frame, text="CBC 模式 (密码分组链)", 
                         font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        # 明文输入
        ttk.Label(frame, text="明文 (字符串):").grid(row=1, column=0, padx=5, pady=5, sticky='ne')
        self.cbc_plaintext = scrolledtext.ScrolledText(frame, height=3, width=50)
        self.cbc_plaintext.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        # 密钥输入
        ttk.Label(frame, text="密钥 (16进制):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.cbc_key = ttk.Entry(frame, width=20)
        self.cbc_key.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        # IV输入
        ttk.Label(frame, text="初始向量IV (16进制):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.cbc_iv = ttk.Entry(frame, width=20)
        self.cbc_iv.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        ttk.Button(frame, text="生成随机IV", command=self.cbc_generate_iv).grid(
            row=3, column=2, padx=5, pady=5, sticky='w')
        
        # 密文输入
        ttk.Label(frame, text="密文 (16进制块):").grid(row=4, column=0, padx=5, pady=5, sticky='ne')
        self.cbc_ciphertext = scrolledtext.ScrolledText(frame, height=3, width=50)
        self.cbc_ciphertext.grid(row=4, column=1, columnspan=2, padx=5, pady=5)
        
        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=10)
        ttk.Button(btn_frame, text="CBC加密", command=self.cbc_encrypt).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="CBC解密", command=self.cbc_decrypt).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="篡改测试", command=self.cbc_tamper_test).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="清空", command=self.cbc_clear).pack(side='left', padx=5)
        
        # 结果显示
        ttk.Label(frame, text="结果:").grid(row=6, column=0, padx=5, pady=5, sticky='ne')
        self.cbc_result = scrolledtext.ScrolledText(frame, height=12, width=70)
        self.cbc_result.grid(row=6, column=1, columnspan=2, padx=5, pady=5)
        
        # 说明
        info = ("说明：\n"
               "1. CBC模式使用初始向量(IV)和前一个密文块进行链接\n"
               "2. 加密: C_i = E_K(P_i ⊕ C_{i-1}), C_0 = IV\n"
               "3. 篡改测试将修改密文块，观察对解密结果的影响")
        ttk.Label(frame, text=info, justify='left', foreground='blue').grid(
            row=7, column=0, columnspan=3, padx=10, pady=10)
    
    def cbc_generate_iv(self):
        """生成随机IV"""
        iv = random.randint(0, 0xFFFF)
        self.cbc_iv.delete(0, tk.END)
        self.cbc_iv.insert(0, f"{iv:04X}")
    
    def cbc_encrypt(self):
        """CBC加密"""
        try:
            plaintext_str = self.cbc_plaintext.get(1.0, tk.END).strip()
            key_str = self.cbc_key.get().strip()
            iv_str = self.cbc_iv.get().strip()
            
            if not plaintext_str or not key_str or not iv_str:
                messagebox.showwarning("警告", "请输入明文、密钥和IV")
                return
            
            key = int(key_str, 16)
            iv = int(iv_str, 16)
            
            if key > 0xFFFF or iv > 0xFFFF:
                messagebox.showerror("错误", "密钥和IV必须是16位（0000-FFFF）")
                return
            
            # 转换为块
            plaintext_blocks = self.saes.string_to_blocks(plaintext_str)
            
            # CBC加密
            ciphertext_blocks = self.saes.cbc_encrypt(plaintext_blocks, key, iv)
            
            # 显示密文
            cipher_str = ' '.join([f"{block:04X}" for block in ciphertext_blocks])
            self.cbc_ciphertext.delete(1.0, tk.END)
            self.cbc_ciphertext.insert(1.0, cipher_str)
            
            # 显示结果
            result = (f"=== CBC加密成功 ===\n"
                     f"明文: {plaintext_str}\n"
                     f"明文块数: {len(plaintext_blocks)}\n"
                     f"密钥: {key:04X}\n"
                     f"初始向量IV: {iv:04X}\n"
                     f"密文块: {cipher_str}\n\n"
                     f"明文块详情:\n")
            
            for i, block in enumerate(plaintext_blocks):
                result += f"  P{i} = {block:04X}\n"
            
            result += f"\n密文块详情:\n"
            for i, block in enumerate(ciphertext_blocks):
                result += f"  C{i} = {block:04X}\n"
            
            self.cbc_result.delete(1.0, tk.END)
            self.cbc_result.insert(tk.END, result)
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数据")
    
    def cbc_decrypt(self):
        """CBC解密"""
        try:
            cipher_str = self.cbc_ciphertext.get(1.0, tk.END).strip()
            key_str = self.cbc_key.get().strip()
            iv_str = self.cbc_iv.get().strip()
            
            if not cipher_str or not key_str or not iv_str:
                messagebox.showwarning("警告", "请输入密文、密钥和IV")
                return
            
            key = int(key_str, 16)
            iv = int(iv_str, 16)
            
            if key > 0xFFFF or iv > 0xFFFF:
                messagebox.showerror("错误", "密钥和IV必须是16位（0000-FFFF）")
                return
            
            # 解析密文块
            cipher_parts = cipher_str.split()
            ciphertext_blocks = [int(block, 16) for block in cipher_parts]
            
            # CBC解密
            plaintext_blocks = self.saes.cbc_decrypt(ciphertext_blocks, key, iv)
            
            # 转换为字符串
            plaintext_str = self.saes.blocks_to_string(plaintext_blocks)
            
            # 显示明文
            self.cbc_plaintext.delete(1.0, tk.END)
            self.cbc_plaintext.insert(1.0, plaintext_str)
            
            # 显示结果
            result = (f"=== CBC解密成功 ===\n"
                     f"密文块数: {len(ciphertext_blocks)}\n"
                     f"密钥: {key:04X}\n"
                     f"初始向量IV: {iv:04X}\n"
                     f"明文: {plaintext_str}\n\n"
                     f"密文块详情:\n")
            
            for i, block in enumerate(ciphertext_blocks):
                result += f"  C{i} = {block:04X}\n"
            
            result += f"\n明文块详情:\n"
            for i, block in enumerate(plaintext_blocks):
                result += f"  P{i} = {block:04X}\n"
            
            self.cbc_result.delete(1.0, tk.END)
            self.cbc_result.insert(tk.END, result)
            
        except ValueError as e:
            messagebox.showerror("错误", f"请输入有效的数据: {str(e)}")
    
    def cbc_tamper_test(self):
        """CBC篡改测试"""
        try:
            cipher_str = self.cbc_ciphertext.get(1.0, tk.END).strip()
            key_str = self.cbc_key.get().strip()
            iv_str = self.cbc_iv.get().strip()
            
            if not cipher_str or not key_str or not iv_str:
                messagebox.showwarning("警告", "请先进行CBC加密")
                return
            
            key = int(key_str, 16)
            iv = int(iv_str, 16)
            
            # 解析密文块
            cipher_parts = cipher_str.split()
            ciphertext_blocks = [int(block, 16) for block in cipher_parts]
            
            if len(ciphertext_blocks) < 2:
                messagebox.showwarning("警告", "密文块数量不足，请使用更长的明文")
                return
            
            # 原始解密
            original_plaintext_blocks = self.saes.cbc_decrypt(ciphertext_blocks, key, iv)
            original_plaintext = self.saes.blocks_to_string(original_plaintext_blocks)
            
            # 篡改第一个密文块（翻转一位）
            tampered_blocks = ciphertext_blocks.copy()
            tampered_blocks[0] ^= 0x0001  # 翻转最低位
            
            # 篡改后解密
            tampered_plaintext_blocks = self.saes.cbc_decrypt(tampered_blocks, key, iv)
            tampered_plaintext = self.saes.blocks_to_string(tampered_plaintext_blocks)
            
            # 显示对比结果
            result = (f"=== CBC篡改测试 ===\n\n"
                     f"原始密文块:\n")
            
            for i, block in enumerate(ciphertext_blocks):
                result += f"  C{i} = {block:04X}\n"
            
            result += f"\n篡改密文块（C0翻转最低位）:\n"
            for i, block in enumerate(tampered_blocks):
                if i == 0:
                    result += f"  C{i} = {block:04X} ← 已篡改\n"
                else:
                    result += f"  C{i} = {block:04X}\n"
            
            result += f"\n原始明文: {original_plaintext}\n"
            result += f"原始明文块:\n"
            for i, block in enumerate(original_plaintext_blocks):
                result += f"  P{i} = {block:04X}\n"
            
            result += f"\n篡改后明文: {tampered_plaintext}\n"
            result += f"篡改后明文块:\n"
            for i, block in enumerate(tampered_plaintext_blocks):
                if block != original_plaintext_blocks[i]:
                    result += f"  P{i} = {block:04X} ← 受影响\n"
                else:
                    result += f"  P{i} = {block:04X}\n"
            
            result += f"\n分析：\n"
            result += f"篡改C0影响了P0和P1的解密结果\n"
            result += f"这展示了CBC模式的错误传播特性\n"
            
            self.cbc_result.delete(1.0, tk.END)
            self.cbc_result.insert(tk.END, result)
            
        except Exception as e:
            messagebox.showerror("错误", f"篡改测试失败: {str(e)}")
    
    def cbc_clear(self):
        """清空CBC界面"""
        self.cbc_plaintext.delete(1.0, tk.END)
        self.cbc_key.delete(0, tk.END)
        self.cbc_iv.delete(0, tk.END)
        self.cbc_ciphertext.delete(1.0, tk.END)
        self.cbc_result.delete(1.0, tk.END)


def main():
    """主函数"""
    root = tk.Tk()
    app = SAESGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
