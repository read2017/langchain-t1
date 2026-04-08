"""
partial()方法可以格式化部分变量，并且继续返回一个模板，通常在部分提示词模板场景下使用
"""
from langchain_core.prompts import PromptTemplate

# 创建模板对象，定义提示词模板格式
# 模板包含两个占位符：role（角色）和 question（问题）
template = PromptTemplate(
    input_variables=["role", "question"],
    template="你是一个{role}，请回答以下问题：{question}"
)

# 使用partial方法固定role参数为"python开发"
# 返回一个新的模板对象，其中role参数已被绑定
partial_template = template.partial(role="python开发")

# 使用新的模板对象格式化question参数，生成最终提示词
formatted_prompt = partial_template.format(question="什么是partial方法？")
print(formatted_prompt)

# 也可以在实例化过程中直接指定partial_variables参数来设置部分变量
template2 = PromptTemplate(
    input_variables=["role", "question"],
    template="你是一个{role}，请回答以下问题：{question}",
    partial_variables={"role": "python开发"}
)
formatted_prompt2 = template2.format(question="什么是partial方法？")
print(formatted_prompt2)
