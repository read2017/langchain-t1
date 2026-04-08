import os 
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model = "qwen-plus",
    model_provider = "openai",
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

questions = [
    "什么是LangChain？",
    "LangChain的核心组件有哪些？",
    "如何使用LangChain构建一个简单的聊天机器人？",
]

responses = model.batch(questions)

# for i, response in enumerate(responses):
#     print(f"问题：{questions[i]}")
#     print(f"回答：{response.content}\n")

for q, r in zip(questions, responses):
    print(f"问题：{q}")
    print(f"回答：{r.content}\n")