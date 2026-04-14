"""
https://bailian.console.aliyun.com/cn-beijing/?tab=api#/api/?type=model&url=2587654
uv add langchain-community dashscope
"""
from langchain_community.embeddings import DashScopeEmbeddings # pyright: ignore[reportMissingImports]

embedding = DashScopeEmbeddings(
    model = "text-embedding-v4",
)

text = "This is a test document."
query_result = embedding.embed_query(text)
print("文本向量长度：", len(query_result), sep="")
doc_result = embedding.embed_documents([
    "This is a test document.",
    "hello world",
    "my name is Reader",
    "I am a computer engineer"
])
print(doc_result)
print("文本向量数量：", len(doc_result), "，文本向量长度：", len(doc_result[0]), sep='')
