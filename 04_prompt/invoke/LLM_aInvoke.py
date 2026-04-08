import os
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage, AIMessage
import asyncio # 引入 asyncio 库以支持异步调用

model = init_chat_model(
    model = "qwen-plus",
    model_provider = "openai",
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

async def main():
    # 异步调用模型
    response = await model.ainvoke("解释一下LangChain是什么，简洁回答100字以内")
    print(f'相应类型：{type(response)}')
    print(f'响应内容：{response.content}')

if __name__ == "__main__":
    asyncio.run(main())