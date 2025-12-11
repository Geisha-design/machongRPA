import tkinter as tk
from tkinter import scrolledtext, ttk
from openai import OpenAI
import threading
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class AIChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI智能问答助手")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 初始化OpenAI客户端
        self.client = self.initialize_client()
        
        # 对话历史
        self.messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'}
        ]
        
        # 流式输出相关变量
        self.is_streaming = False
        self.current_stream_text = ""
        self.stream_message_index = None
        
        # 创建界面
        self.create_widgets()
        
        # 设置样式
        self.setup_styles()
        
    def initialize_client(self):
        """初始化OpenAI客户端"""
        try:
            client = OpenAI(
                api_key="sk-5c50af7dc8b94023a5f01d060550f026",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
            return client
        except Exception as e:
            self.show_error(f"初始化客户端失败：{e}")
            return None

    def setup_styles(self):
        """设置界面样式"""
        self.root.configure(bg='#f0f0f0')
        
        # 配置标签样式
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("微软雅黑", 16, "bold"), foreground="#2c3e50")
        self.style.configure("Info.TLabel", font=("微软雅黑", 10), foreground="#7f8c8d")
        
        # 配置按钮样式
        self.style.configure("Action.TButton", font=("微软雅黑", 10, "bold"), padding=6)
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="AI智能问答助手", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        # 聊天显示区域
        chat_frame = ttk.LabelFrame(main_frame, text="对话记录", padding="5")
        chat_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            width=70, 
            height=20,
            font=("微软雅黑", 11),
            state=tk.DISABLED
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text="您的问题", padding="5")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.user_input = tk.Text(input_frame, height=4, font=("微软雅黑", 11))
        self.user_input.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.user_input.bind("<Return>", self.on_enter_press)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        # 发送按钮
        self.send_button = ttk.Button(
            button_frame, 
            text="发送 (Enter)", 
            command=self.send_message,
            style="Action.TButton"
        )
        self.send_button.grid(row=0, column=0, padx=(0, 5), sticky=tk.E)
        
        # 清屏按钮
        clear_button = ttk.Button(
            button_frame, 
            text="清屏", 
            command=self.clear_chat,
            style="Action.TButton"
        )
        clear_button.grid(row=0, column=1, padx=5)
        
        # 退出按钮
        exit_button = ttk.Button(
            button_frame, 
            text="退出", 
            command=self.root.quit,
            style="Action.TButton"
        )
        exit_button.grid(row=0, column=2, padx=(5, 0), sticky=tk.W)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, style="Info.TLabel")
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 添加初始消息
        self.add_to_chat("AI助手", "您好！我是AI智能问答助手，有什么我可以帮您的吗？", "assistant")
        
    def on_enter_press(self, event):
        """处理回车键事件"""
        if event.state & 0x1:  # Shift键被按下
            # 插入换行符
            self.user_input.insert(tk.INSERT, "\n")
            return "break"
        else:
            # 发送消息
            self.send_message()
            return "break"
            
    def send_message(self):
        """发送用户消息"""
        # 获取用户输入
        user_text = self.user_input.get("1.0", tk.END).strip()
        
        if not user_text:
            return
            
        # 添加到聊天记录
        self.add_to_chat("您", user_text, "user")
        
        # 清空输入框
        self.user_input.delete("1.0", tk.END)
        
        # 更新状态
        self.status_var.set("AI正在思考...")
        self.send_button.config(state=tk.DISABLED)
        
        # 在新线程中获取AI回复
        threading.Thread(target=self.get_ai_response, args=(user_text,), daemon=True).start()
        
    def get_ai_response(self, user_text):
        """在新线程中获取AI回复（流式）"""
        try:
            # 添加用户消息到对话历史
            self.messages.append({'role': 'user', 'content': user_text})
            
            # 初始化流式输出变量
            self.is_streaming = True
            self.current_stream_text = ""
            
            # 在聊天显示区创建一个新的AI消息位置
            self.root.after(0, self.init_stream_display)
            
            # 获取AI回复（流式）
            stream = self.client.chat.completions.create(
                model="qwen-plus",
                messages=self.messages,
                stream=True
            )
            
            # 处理流式响应
            for chunk in stream:
                if not self.is_streaming:  # 如果用户中断了流
                    break
                    
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    self.current_stream_text += content
                    # 在主线程中更新UI
                    self.root.after(0, self.update_stream_display, content)
                    
            # 流完成，保存完整消息
            if self.current_stream_text:
                self.messages.append({'role': 'assistant', 'content': self.current_stream_text})
                
            # 结束流式输出
            self.root.after(0, self.finish_stream_display)
            
        except Exception as e:
            error_msg = f"获取AI回复时出错：{str(e)}"
            self.is_streaming = False
            self.root.after(0, self.add_to_chat, "系统", error_msg, "system")
            self.root.after(0, self.restore_ui_state)
            
        finally:
            # 确保UI状态恢复正常
            if self.is_streaming:  # 只有在未被中断的情况下才恢复状态
                self.is_streaming = False
                self.root.after(0, self.restore_ui_state)
                
    def init_stream_display(self):
        """初始化流式显示"""
        self.chat_display.config(state=tk.NORMAL)
        
        # 添加AI助手名称
        self.chat_display.insert(tk.END, f"AI助手:\n", "ai_name")
        
        # 记录流消息的起始位置
        self.stream_message_index = self.chat_display.index(tk.END)
        
        # 添加初始文本
        self.chat_display.insert(tk.END, f"", "ai_message")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def update_stream_display(self, content):
        """更新流式显示"""
        if not self.stream_message_index:
            return
            
        self.chat_display.config(state=tk.NORMAL)
        
        # 插入新内容到流消息位置
        self.chat_display.insert(self.stream_message_index, content, "ai_message")
        
        # 更新流消息位置
        self.stream_message_index = self.chat_display.index(tk.END)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def finish_stream_display(self):
        """完成流式显示"""
        self.chat_display.config(state=tk.NORMAL)
        
        # 添加换行和空行以分隔下一条消息
        self.chat_display.insert(tk.END, "\n\n", "ai_message")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def restore_ui_state(self):
        """恢复UI状态"""
        self.status_var.set("就绪")
        self.send_button.config(state=tk.NORMAL)
        
    def add_to_chat(self, sender, message, role):
        """添加消息到聊天记录"""
        self.chat_display.config(state=tk.NORMAL)
        
        # 根据角色设置不同的显示样式
        if role == "user":
            tag = "user_message"
            self.chat_display.insert(tk.END, f"{sender}:\n", "user_name")
            self.chat_display.insert(tk.END, f"{message}\n\n", tag)
        elif role == "assistant":
            tag = "ai_message"
            self.chat_display.insert(tk.END, f"{sender}:\n", "ai_name")
            self.chat_display.insert(tk.END, f"{message}\n\n", tag)
        else:
            tag = "system_message"
            self.chat_display.insert(tk.END, f"{sender}:\n", "system_name")
            self.chat_display.insert(tk.END, f"{message}\n\n", tag)
            
        # 配置标签样式
        self.chat_display.tag_config("user_name", foreground="#2980b9", font=("微软雅黑", 10, "bold"))
        self.chat_display.tag_config("ai_name", foreground="#27ae60", font=("微软雅黑", 10, "bold"))
        self.chat_display.tag_config("system_name", foreground="#e74c3c", font=("微软雅黑", 10, "bold"))
        self.chat_display.tag_config("user_message", foreground="#2980b9", font=("微软雅黑", 10))
        self.chat_display.tag_config("ai_message", foreground="#27ae60", font=("微软雅黑", 10))
        self.chat_display.tag_config("system_message", foreground="#e74c3c", font=("微软雅黑", 10))
        
        self.chat_display.config(state=tk.DISABLED)
        
        # 滚动到最新消息
        self.chat_display.see(tk.END)
        
    def clear_chat(self):
        """清空聊天记录"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_to_chat("AI助手", "对话记录已清空。有什么我可以帮您的吗？", "assistant")
        
    def show_error(self, message):
        """显示错误信息"""
        self.add_to_chat("系统", message, "system")

def main():
    root = tk.Tk()
    app = AIChatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()