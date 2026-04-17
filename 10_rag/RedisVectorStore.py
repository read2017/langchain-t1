import os
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document

# 1. 环境准备：配置 API Key
# 建议通过环境变量获取，保护隐私
# os.environ["DASHSCOPE_API_KEY"] = "你的Key" 

# 2. 初始化 Embedding 模型
# 选择 text-embedding-v3，它能将文本转化为 1024 或 1536 维的向量
embeddings_model = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv('DASHSCOPE_API_KEY')
    )

# 3. 准备数据：使用 LangChain 的标准 Document 结构
# 相比直接传文本，Document 结构能清晰地将“内容”与“元数据”绑定
raw_data = [
    {"text": "我喜欢吃苹果", "source": "个人喜好", "category": "水果"},
    {"text": "苹果是我最喜欢吃的水果", "source": "百科", "category": "水果"},
    {"text": "我喜欢用苹果手机", "source": "数码论坛", "category": "科技"},
]

documents = [
    Document(
        page_content=item["text"], 
        metadata={"source": item["source"], "category": item["category"]}
    ) for item in raw_data
]

# ---------------------------------------------------------
# 理解 Embedding：我们可以手动看看第一条数据转成向量后长啥样
# ---------------------------------------------------------
sample_vector = embeddings_model.embed_query(documents[0].page_content)
print(f"--- 向量化展示 ---")
print(f"文本内容: {documents[0].page_content}")
print(f"向量维度: {len(sample_vector)}") # v3 通常是 1536 维
print(f"前 3 个数值: {sample_vector[:3]} ... (这是一个超长列表)")
print("-" * 30)

# 4. 配置 Redis 向量存储
# index_name: 相当于数据库的表名
# redis_url: 你的 Redis 连接地址
config = RedisConfig(
    index_name="user_preferences",
    redis_url="redis://localhost:6379",
)

# 5. 一键存储
# 这一步在后台做了三件事：
# a. 调用模型把所有 Document 的 text 转成向量
# b. 将文本、元数据、向量打包
# c. 存入 Redis 并建立 HNSW 索引
vector_store = RedisVectorStore.from_documents(
    documents=documents,
    embedding=embeddings_model,
    config=config
)

print("✅ 数据已成功存入 Redis 向量库")

# 6. 验证：简单的相似度搜索
query = "我最近想换个手机"
results = vector_store.similarity_search(query, k=1)

print(f"\n--- 搜索测试 ---")
print(f"提问: {query}")
print(f"最匹配内容: {results[0].page_content}")
print(f"对应的元数据: {results[0].metadata}")