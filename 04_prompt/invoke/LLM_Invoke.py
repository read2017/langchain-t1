import os
# form dotenv import load_dotenv 
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
    HumanMessage(content="简单介绍下广告法，一句话告知50字以内"),
]

response = model.invoke(messages)
print(f"响应类型：{type(response)}")
print(f"响应内容：{response.content}")
print(response.content_blocks) # 以块的形式返回响应内容，适用于流式输出
