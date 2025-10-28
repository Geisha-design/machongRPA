# # async_batch.py
# import asyncio
# from volcenginesdkarkruntime import AsyncArk
#
# client = AsyncArk(api_key="你的ARK_API_KEY")
#
# async def one_round(q: str) -> str:
#     resp = await client.chat.completions.create(
#         model="doubao-1-5-pro-32k-250115",
#         messages=[{"role": "user", "content": q}]
#     )
#     return resp.choices[0].message.content
#
# async def main():
#     questions = ["1+1=", "Python 之父是谁？", "火山引擎总部在哪？"]
#     results = await asyncio.gather(*(one_round(q) for q in questions))
#     for q, a in zip(questions, results):
#         print(f"Q: {q}  A: {a}")
#
# if __name__ == "__main__":
#     asyncio.run(main())


# 2. openai_to_huoshan.py
# from openai import OpenAI
#
# client = OpenAI(
#     api_key="c985dcd3-ef0d-4efe-8a86-76adb88af288",
#     base_url="https://ark.cn-beijing.volces.com/api/v3"  # 关键：把指向火山
# )
#
# resp = client.chat.completions.create(
#     model="bot-20250509172556-w54xh",  # 这里写你的接入点ID
#     messages=[{"role": "user", "content": " Python 有什么优点？"}],
#     stream=False
# )
#
# print(resp.choices[0].message.content)
#
#



# （（（（（（（（（（

import os
from openai import OpenAI

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Openai客户端，从环境变量中读取您的API Key
client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    # 从环境变量中获取您的 API Key
    api_key="c985dcd3-ef0d-4efe-8a86-76adb88af288"
    # os.environ.get("ARK_API_KEY")
)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model="bot-20250509172556-w54xh",  # bot-20250509172556-w54xh 为您当前的智能体的ID，注意此处与Chat API存在差异。差异对比详见 SDK使用指南
    messages=[
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
)
print(completion.choices[0].message.content)
if hasattr(completion, "references"):
    print(completion.references)


# Multi-round：
print("----- multiple rounds request -----")
completion = client.chat.completions.create(
    model="bot-20250509172556-w54xh",  # bot-20250509172556-w54xh 为您当前的智能体的ID，注意此处与Chat API存在差异。差异对比详见 SDK使用指南
    messages=[  # 通过会话传递历史信息，模型会参考上下文消息
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "花椰菜是什么？"},
        {"role": "assistant", "content": "花椰菜又称菜花、花菜，是一种常见的蔬菜。"},
        {"role": "user", "content": "再详细点"},
    ],
)
print(completion.choices[0].message.content)
if hasattr(completion, "references"):
    print(completion.references)

# Streaming:
print("----- streaming request -----")
stream = client.chat.completions.create(
    model="bot-20250509172556-w54xh",  # bot-20250509172556-w54xh 为您当前的智能体的ID，注意此处与Chat API存在差异。差异对比详见 SDK使用指南
    messages=[
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "常见的十字花科植物有哪些？"},
    ],
    stream=True,
)
for chunk in stream:
    if hasattr(chunk, "references"):
        print(chunk.references)
    if not chunk.choices:
        continue
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
print()
