# from langchain_core.prompts import load_prompt
# import os

# # 获取当前目录下的prompt.json文件
# current_dir = os.path.dirname(os.path.abspath(__file__))
# prompt_path = os.path.join(current_dir, "prompt.json")
# print(prompt_path)
# # 加载prompt.json文件中的提示词模板
# template = load_prompt(prompt_path, encoding="utf-8")
# formatted_prompt = template.format(name = "张三", what = "搞笑的")
'''
LangChainDeprecationWarning: The function `load_prompt` was deprecated in LangChain 1.2.21 and will be removed in 2.0.0. Use `Use `dumpd`/`dumps` from `langchain_core.load` to serialize prompts and `load`/`loads` to deserialize them.` instead.
这个警告告诉你：LangChain 正在清理旧的代码库，load_prompt 这个老函数即将被淘汰（在 2.0.0 版本彻底移除）。

简单来说，官方现在希望你统一使用 langchain_core 中的序列化工具。

'''

import json
from langchain_core.load import load
from langchain_core.prompts import PromptTemplate
import os

# 获取当前目录下的prompt.json文件
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(current_dir, "prompt.json")

# 步骤：
# 1. 先用标准的 json 库读取文件内容
with open(prompt_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# 2. 使用 load 函数将字典转换为 LangChain 的 PromptTemplate 对象
# prompt = load(json_data)  # 直接传入 JSON 字符串，load 本应该会自动解析并创建 PromptTemplate 对象，但是返回仍然是str，因为load对json格式要求严格，需要特额定的格式才能正确识别并转换为PromptTemplate对象
# print("prompt类型：", type(prompt)) # 输出：prompt类型： <class 'dict'>，说明load函数没有正确解析json数据并创建PromptTemplate对象，而是直接返回了原始的字符串内容


# 方法一：先解析出json数据，再用PromptTemplate创建对象
template = PromptTemplate(
    input_variables = json_data["input_variables"],
    template = json_data["template"]
)
print("模板类型：", type(template))
formatted_prompt = template.format(name = "张三", what = "搞笑的")
print("格式化后的提示词：", formatted_prompt)


