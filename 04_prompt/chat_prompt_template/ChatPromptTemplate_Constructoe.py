"""
使用ChatPromptTemplate构造方法直接实例化
实例化时需要传入messages: Sequence[MessageLikeRepresentation]
messages 参数支持如下格式：
	tuple 构成的列表，格式为[(role, content)]
	dict 构成的列表，格式为[{“role”:... , “content”:...}]
	Message 类构成的列表
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
import os

# 创建聊天提示模板，包含系统角色设定和用户问题输入
prompt = ChatPromptTemplate(
    [
    ("system", "你是一个{role}，请简短回答我提出的问题"),
    ("user", "请回答：{question}")
    ]
)
# 使用指定的角色和问题生成具体的提示内容
formatted_prompt = prompt.format_messages(role="AI助手", question="什么是langchain？20字以内")
print(f"生成的提示词：{formatted_prompt}")

llm = init_chat_model(
    model = "qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
response = llm.invoke(formatted_prompt)
print(f"模型返回的原始响应：{response}")
print("原始响应的类型：", type(response))