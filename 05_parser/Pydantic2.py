import os
from typing import List
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

# 1. 初始化模型
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 2. 使用 Pydantic 定义数据模型
# Field 的 description 会被放入 JSON Schema，直接引导模型生成
class UserInfo(BaseModel):
    name: str = Field(..., description="用户的姓名")
    age: int = Field(..., description="用户的年龄")

class UserList(BaseModel):
    users: List[UserInfo] = Field(..., description="包含多个用户信息的列表")

# 3. 构造结构化输出模型
# method="function_calling" 通常比默认设置在 Qwen 上更稳定
model_with_structured_output = model.with_structured_output(UserList, method="function_calling")

# 4. 调用
messages = [
    {"role": "system", "content": "你是一个严谨的数据助手。"},
    {"role": "user", "content": "任意生成三个用户，包括他们的姓名和年龄。"}
]

response = model_with_structured_output.invoke(messages)

# 5. 打印结果
print("模型返回的结构化响应：", response)
print("解析结果的类型：", type(response))

# 如果你想直接访问数据，现在可以像操作对象一样操作它
for user in response.users:
    print(f"姓名: {user.name}, 年龄: {user.age}")