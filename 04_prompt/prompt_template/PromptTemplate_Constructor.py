import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate


# 创建一个PromptTemplate对象，用于生成格式化的提示词模板
# 该模板包含两个变量：role（角色）和question（问题）
template = PromptTemplate(
    input_variables=["role", "question"],
    template="你是一个专业的{role}，请回答以下问题：{question}"
)
template2 = PromptTemplate(
    input_variables=["length"],
    template="内容不超过{length}个字"
)

combined_prompt = template + template2
# 使用模板格式化具体的提示词内容
# 将role替换为"python开发"，question替换为"冒泡排序怎么写？"
formatted_prompt = combined_prompt.format(role="python开发", question="冒泡排序怎么写？", length=100)

# 输出格式化后的提示词内容
print(formatted_prompt)
# # 初始化一个聊天模型，使用OpenAI的qwen-plus模型
# model = init_chat_model(
#     model = "qwen-plus",
#     model_provider = "openai",
#     api_key = os.getenv("DASHSCOPE_API_KEY"),
#     base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
# )
# # 使用模型的invoke方法，传入格式化后的提示词内容，获取模型的响应
# response = model.invoke(formatted_prompt)
# # 输出模型的响应内容
# print(response.content)

