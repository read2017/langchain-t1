"""
RunnableSerializable-串行链
子链叠加串行，假如我们需要多次调用大模型，将多个步骤串联起来实现功能
"""
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
import os
from loguru import logger
model = init_chat_model(
    model = "qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
    ("user", "请回答：{question}")
]
)

parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译助手，将用户输入的内容翻译成英文"),
    ("user", "请翻译：{input}")
]
)
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2
# 组合成一个复合 Chain，使用 lambda 函数将chain1执行结果content内容添加input键作为参数传递给chain2
full_chain = {"question": RunnablePassthrough()} | chain1 | (lambda x: {"input": x}) | chain2
# 直接调用复合 Chain，传入问题参数，得到最终翻译后的英文输出
final_output = full_chain.invoke({"question": "什么是AI？"})
logger.info(f"最终输出：{final_output}")