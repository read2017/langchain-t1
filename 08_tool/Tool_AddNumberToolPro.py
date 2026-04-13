'''
使用@tool装饰器
装饰器默认使用函数名称作为工具名称，但可以通过参数name_or_callable 来覆盖此设置。
同时，装饰器将使用函数的文档字符串作为工具的描述，因此函数必须提供文档字符串
'''

'''
需求：
定义了一个名为add_number的工具函数，用于执行两个整数相加操作。主要功能包括：

使用Pydantic定义参数模型FieldInfo，指定两个整数参数a和b
通过@tool装饰器将函数注册为LangChain工具，绑定参数schema
打印工具的元信息（名称、参数、描述等）并调用工具执行加法运算并输出结果
'''
from langchain.tools import tool
from loguru import logger
from pydantic import BaseModel, Field
# 使用Pydantic定义参数模型FieldInfo，指定两个整数参数a和b
class FieldInfo(BaseModel):
    a: int = Field(..., description="第一个整数")
    b: int = Field(..., description="第二个整数")

@tool(name_or_callable="add_numbers", description="将两个整数相加并返回结果", args_schema=FieldInfo)
def add_numbers(a: int, b: int) -> int:
    """将两个数字相加并返回结果"""
    return a + b

result = add_numbers.invoke({"a": 5, "b": 10})
print(result)  # 输出: 15
logger.info(f"name = {add_numbers.name}")
logger.info(f"description = {add_numbers.description}")
logger.info(f"args = {add_numbers.args}")
logger.info(f"return_direct = {add_numbers.return_direct}")