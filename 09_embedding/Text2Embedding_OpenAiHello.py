import os
from openai import OpenAI

input = "衣服质量杠杠滴"

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

response = client.embeddings.create(
    input=input,
    model="text-embedding-v4",
)

print(response.model_dump_json(indent=4))