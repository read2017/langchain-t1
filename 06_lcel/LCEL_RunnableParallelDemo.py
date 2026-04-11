"""
RunnableParallel-并行链

在 Langchain 中，创建并行链（Parallel Chains），是指同时运行多个子链（Chain），并在它们都完成后汇总结果。
**作用**：同时执行多个 Runnable，合并结果
"""
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough, RunnableParallel
import os
from loguru import logger

# 1. 定义底层模型
model = init_chat_model(
    model = "qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 2. 定义不同分支的 Prompt
prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
    ("user", "请回答：{question}")
])
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

# 并行链2提示词
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用英文简短回答"),
    ("human", "请简短介绍什么是{question}")
])
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

# 3. 构建 RunnableParallel
parallel_chain = RunnableParallel(
    {
        "中文回答": chain1,
        "英文回答": chain2
    }
)

# 4. 直接调用并行链，传入参数，得到一个包含两个分支结果的列表
final_output = parallel_chain.invoke({"question": "什么是AI？"})
logger.info(f"并行链的最终输出：{final_output}")