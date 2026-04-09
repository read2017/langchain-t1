import os
from typing import TypedDict, Annotated
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model = "qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

class UserInfo(TypedDict):
    name: Annotated[str, "用户的姓名"]
    age: Annotated[int, "用户的年龄"]

class UserList(TypedDict):
    users: Annotated[list[UserInfo], "用户姓名和年龄列表"]

messages = [
    {'role': 'system', 'content': '你是一个用户信息生成器，请根据用户的要求生成相应的用户信息，返回格式必须符合以下要求：{"users": [{"name": "姓名", "age": 年龄}]}'},
    {"role": "user", "content": "任意生成三个用户,包括他们的姓名和年龄"}
]

model_with_structured_output = model.with_structured_output(UserList)
response = model_with_structured_output.invoke(messages)
print("模型返回的结构化响应：", response)
print("解析结果的类型：", type(response))

# 模型返回的结构化响应： {'users': [{'name': '张伟'}]} 输出结果不对，被吞掉了age字段，说明模型没有正确理解提示词中的格式要求，导致生成的输出不符合预期的结构化格式。
# Annotated类型提示在这里没有被模型正确解析和应用，可能是因为模型对提示词中的格式要求理解不够清晰，建议改用Pydantic进行更严格的类型定义和验证，以确保生成的输出符合预期的结构化格式。
# 解析结果的类型： <class 'dict'>


# import os
# from typing import TypedDict, Annotated
# from langchain.chat_models import init_chat_model

# llm = init_chat_model(
#     model="qwen-plus",
#     model_provider="openai",
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )

# class Animal(TypedDict):
#     animal: Annotated[str, "动物"]
#     emoji: Annotated[str, "表情"]

# class AnimalList(TypedDict):
#     animals: Annotated[list[Animal], "动物与表情列表"] # List&lt;Animal&gt;

# messages = [{"role": "user", "content": "任意生成三种动物，以及他们的 emoji 表情"}]

# llm_with_structured_output = llm.with_structured_output(AnimalList)
# resp = llm_with_structured_output.invoke(messages)
# print(resp)