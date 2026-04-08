# 方式2：使用 from_template 方法实例化提示词模板
from langchain_core import PromptTemplate

# 创建一个PromptTemplate对象，用于生成格式化的提示词模板
# 模板包含两个占位符：{role}表示角色，{question}表示问题
template = PromptTemplate.from_template("你是一个专业的{role}，请回答以下问题：{question}")

# 使用指定的角色和问题参数来格式化模板，生成最终的提示词字符串
# role: 工程师角色描述
# question: 具体的技术问题
formatted_prompt = template.format(role="python开发", question="冒泡排序怎么写？")
# 输出格式化后的提示词内容
print(formatted_prompt)
# 输出结果：你是一个专业的python开发，请回答以下问题：冒泡排序怎么写？