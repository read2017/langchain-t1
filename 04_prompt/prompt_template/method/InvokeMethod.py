"""
invoke() 是 LangChain Expression Language（LCEL 的统一执行入口，用于执行任意可运行对象（Runnable ）。返回的是一个 PromptValue 对象，
可以用 .to_string() 或 .to_messages() 查看内容
"""
from langchain_core.prompts import PromptTemplate
# 创建一个PromptTemplate对象，用于生成格式化的提示词模板
# 模板中包含两个占位符：{role}表示角色，{question}表示问题
template = PromptTemplate.from_template(
    # input_variables=["role", "question"],
    "你是一个{role}，请回答以下问题：{question}"
)
# 使用invoke方法执行模板，传入具体的参数值，生成最终的提示词
prompt = template.invoke({"role": "python开发", "question": "什么是invoke方法？"})
# 输出生成的提示词内容# 打印PromptValue对象及其类型
print(prompt)
print(type(prompt))
print()

# 将PromptValue对象转换为字符串并打印
# to_string()方法将PromptValue转换为可读的字符串格式
print(prompt.to_string())
print(type(prompt.to_string()))
print()