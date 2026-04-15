from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.documents import Document
import os

# 1. 初始化阿里千问 Embedding 模型
embedding = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
)

# 2. 准备要向量化的文本（Document 列表）
texts = [
    "通义千问是阿里巴巴研发的大语言模型。",
    "Redis 是一个高性能的键值存储系统，支持向量检索。",
    "LangChain 可以轻松集成各种大模型和向量数据库。"
]
documents = [Document(page_content=text, metadata={"source": "manual"}) for text in texts]

# 3. 创建 Redis 向量存储
vectorstore = Redis.from_documents(
    documents=documents,
    embedding=embedding,
    index_name="my-index1",
    redis_url="redis://localhost:6379",
)

# 4. （可选）后续可直接用于检索
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
results = retriever.invoke("LangChain 和 Redis 怎么结合？")
for res in results:
    print(res.page_content)