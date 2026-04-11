"""
分支链
在LangChain中提供了类RunnableBranch来完成LCEL中的条件分支判断，它可以根据输入的不同采用不同的处理逻辑，
具体示例如下
1. 核心概念
RunnableBranch 接收一组 (条件, 分支路径) 的元组，以及一个 默认路径。

条件 (Condition)：一个函数或 Lambda 表达式，返回 True 或 False。

分支路径 (Runnable)：当对应条件为 True 时执行的逻辑。

默认路径 (Default)：如果前面的所有条件都不满足，则执行这条路径。
"""
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
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
order_prompt = ChatPromptTemplate.from_template("你是一位资深订单管理员。给用户说明你的身份，然后处理以下订单问题（50字以内）：{input}")
tech_prompt = ChatPromptTemplate.from_template("你是一位技术支持专家。给用户说明你的身份，然后解决以下技术难题（50字以内）：{input}")
general_prompt = ChatPromptTemplate.from_template("你是一位友好的助手。给用户说明你的身份，然后回答以下问题（50字以内）：{input}")

# 3. 定义具体的分支链
order_chain = order_prompt | model | StrOutputParser()
tech_chain = tech_prompt | model | StrOutputParser()
general_chain = general_prompt | model | StrOutputParser()

# 4. 定义分类逻辑（这里我们先用一个简单的判断函数）
def classify_intent(input_text):
    input_text = input_text.lower()
    if "订单" in input_text or "快递" in input_text:
        return "order"
    elif "电脑" in input_text or "报错" in input_text or "代码" in input_text:
        return "tech"
    else:
        return "general"

# 5. 构建 RunnableBranch
branch = RunnableBranch(
    (lambda x: classify_intent(x["input"]) == "order", order_chain),
    (lambda x: classify_intent(x["input"]) == "tech", tech_chain),
    general_chain # 最后一个是默认路径
)

# 6. 组合成最终的 Chain
full_chain = {"input": RunnablePassthrough()} | branch

# --- 测试 ---
print("--- 测试订单分支 ---")
print(full_chain.invoke("我的订单什么时候发货？"))

print("\n--- 测试技术分支 ---")
print(full_chain.invoke("这段 Python 代码报错怎么解决？"))

print("\n--- 测试默认分支 ---")
print(full_chain.invoke("今天天气怎么样？"))