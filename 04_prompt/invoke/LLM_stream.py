import os
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage, AIMessage

model = init_chat_model(
    model = "qwen-plus",
    model_provider = "openai",
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

messages = [
    SystemMessage(content="你是一个法律助手，只回答法律问题，超出范围的统一回答，非法律问题无可奉告"),
    HumanMessage(content="简单介绍下婚姻法，一句话告知200字以内"),
]

response = model.stream(messages)
print(f"响应类型：{type(response)}")
for chunk in response:
    print(chunk.content, end='', flush=True) # 以流式的方式输出响应内容，适用于长文本或需要实时输出的场景
