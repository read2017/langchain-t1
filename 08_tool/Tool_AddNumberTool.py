from langchain.tools import tool

@tool
def add_numbers(a: int, b: int) -> int:
    """将两个数字相加并返回结果"""
    return a + b

result = add_numbers.invoke({"a": 5, "b": 10})
print(result)  # 输出: 15
print(f"{add_numbers.name=}\n{add_numbers.description=}\n{add_numbers.args=}")