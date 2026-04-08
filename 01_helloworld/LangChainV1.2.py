import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

my_key = "sk-07fcbafef536494cbab9765b12b97820"
model = init_chat_model(
    model = "qwen-plus",
    model_provider = "openai",
    api_key = my_key,
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1", # SDK 1.2.0 版本新增参数，兼容旧版本 SDK 的接口地址，默认值为 "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# print(model.invoke("Hello, world!").content)

load_dotenv(encoding='utf-8')
model2 = init_chat_model(
    model = "deepseek-v3",
    model_provider = "openai",
    api_key = my_key,
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# print(model2.invoke("你是谁").content)
# model.stream()流式输出