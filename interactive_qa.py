import os
from openai import OpenAI


def initialize_client():
    """初始化OpenAI客户端"""
    try:
        client = OpenAI(
            # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
            # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
            api_key="sk-5c50af7dc8b94023a5f01d060550f026",
            # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        return client
    except Exception as e:
        print(f"初始化客户端失败：{e}")
        return None


def get_ai_response(client, messages):
    """获取AI回复"""
    try:
        completion = client.chat.completions.create(
            model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"获取AI回复时出错：{e}")
        return "抱歉，我无法回答这个问题。"


def interactive_qa():
    """交互式问答主函数"""
    client = initialize_client()
    if not client:
        print("客户端初始化失败，程序退出。")
        return

    # 初始化对话历史
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'}
    ]

    print("欢迎使用交互式问答系统！")
    print("输入 'quit' 或 'exit' 退出程序。")
    print("-" * 40)

    while True:
        try:
            # 获取用户输入
            user_input = input("\n请输入您的问题: ").strip()

            # 检查退出条件
            if user_input.lower() in ['quit', 'exit']:
                print("感谢使用，再见！")
                break

            # 如果输入为空，提示用户重新输入
            if not user_input:
                print("请输入有效问题。")
                continue

            # 添加用户消息到对话历史
            messages.append({'role': 'user', 'content': user_input})

            # 获取AI回复
            print("AI正在思考...")
            ai_response = get_ai_response(client, messages)

            # 显示AI回复
            print(f"AI回复: {ai_response}")

            # 添加AI回复到对话历史
            messages.append({'role': 'assistant', 'content': ai_response})

        except KeyboardInterrupt:
            print("\n\n程序被用户中断，再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    interactive_qa()