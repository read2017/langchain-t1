import os
from langchain.chat_models import init_chat_model
import asyncio # 引入 asyncio 库以支持异步调用

model = init_chat_model(
    model = "qwen-plus",
    model_provider = "openai",
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)
questions = [
    "什么是LangChain？简洁回答，字数控制在100以内",
    "LangChain的核心组件有哪些？简洁回答，字数控制在100以内",
    "如何使用LangChain构建一个简单的聊天机器人？简洁回答，字数控制在100以内",
]

async def async_batch_call():
    responses = await model.abatch(questions)
    for q, r in zip(questions, responses):
        print(f"问题：{q}")
        print(f"回答：{r.content}\n")

if __name__ == "__main__":
    asyncio.run(async_batch_call())
