"""
顺序链
LangChain 的一个典型链条由Prompt、Model、OutputParser （可没有）组成，
然后可以通过 链（Chain） 把它们顺序组合起来，让一个任务的输出成为下一个任务的输入
意思等价于Linux里面的管道符
"""
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from loguru import logger

# 创建聊天提示模板，包含系统角色设定和用户问题输入
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请简短回答我提出的问题"),
    ("user", "请回答：{question}")
])

# 使用指定的角色和问题生成具体的提示内容
formatted_prompt = prompt.invoke(input={"role": "AI助手", "question": "什么是langgraph？50字以内"})
logger.info(f"生成的提示词：{formatted_prompt}")

# 初始化聊天模型，这里使用了一个名为"qwen-plus"的模型，提供者是OpenAI，API密钥从环境变量中获取，base_url指定了模型的访问地址
model = init_chat_model(
    model = "qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 发送提示词给模型并获取响应
response = model.invoke(formatted_prompt)
logger.info(f"模型返回的原始响应：{response}")

# 创建StrOutputParser对象
str_parser = StrOutputParser()
# 使用StrOutputParser解析模型的响应，提取出content字段并转换为字符串输出
parsed_output = str_parser.invoke(response)
logger.info(f"解析后的字符串输出：{parsed_output}")
# 打印类型
print("解析结果的类型：", type(parsed_output))

print("-" * 50)

# 构建处理链：提示模板 -&gt; 模型 -&gt; 输出解析器
chain = prompt | model | str_parser

# 直接调用链，传入参数，得到最终解析后的字符串输出
final_output = chain.invoke({"role": "AI助手", "question": "什么是langgraph？50字以内"})
logger.info(f"链式调用的最终输出：{final_output}")
# 打印类型
print("链式调用结果的类型：", type(final_output))