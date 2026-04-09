"""
JsonOutputParser，即JSON输出解析器，
是一种用于将大模型的自由文本输出转换为结构化JSON数据的工具。

本案例是：指定提示词指明返回 json 格式
"""

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
import os
from loguru import logger
# 创建聊天提示模板，包含系统角色设定和用户问题输入
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请简短回答我提出的问题，结果返回json格式，q字段表示问题，a字段表示答案。"),
    ("user", "请回答：{question}")
])

# 使用指定的角色和问题生成具体的提示内容
formatted_prompt = prompt.format(role="AI助手", question="什么是langchain？200字以内")
logger.info(f"生成的提示词：{formatted_prompt}")
# 初始化聊天模型，这里使用了一个名为
model = init_chat_model(
    model = "qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
# 发送提示词给模型并获取响应
response = model.invoke(formatted_prompt)
logger.info(f"模型返回的原始响应：{response}")

# 分割线
print("-" * 50)

# 创建JsonOutputParser对象
json_parser = JsonOutputParser()
# 使用JsonOutputParser解析模型的响应，提取出结构化的JSON数据
parsed_output = json_parser.invoke(response)
logger.info(f"解析后的JSON数据：{parsed_output}")
# 打印类型
print("解析结果的类型：", type(parsed_output))