# 方式3：部分提示词模板(partial_variables),实例化过程中指定 partial_variables 参数
from langchain_core.prompts import PromptTemplate
from datetime import datetime
import time

# 1 实例化过程中指定 partial_variables 参数
# 创建一个包含时间变量的模板，时间变量使用partial_variables预设为当前时间,然后格式化问题生成最终提示词
template = PromptTemplate(
    input_variables = ["question"],
    template = "现在的时间是{current_time}，请回答以下问题：{question}",
    partial_variables = {"current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
)
formatted_prompt = template.format(question="现在几点了？")
print(formatted_prompt)

# 2 也可以在实例化后，使用 partial_variables 方法设置部分变量
template2 = PromptTemplate(
    input_variables = ["question"],
    template = "现在的时间是{current_time}，请回答以下问题：{question}"
)
# 设置部分变量 current_time 的值为当前时间
template2 = template2.partial(current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
formatted_prompt2 = template2.format(question="现在几点了？")
print(formatted_prompt2)

