from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
import os

# 1. 连接到现有的模型和 Redis 索引
embeddings_model = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv('DASHSCOPE_API_KEY')
    )
config = RedisConfig(
    index_name="user_preferences",    # 必须和存储时定义的名称一致
    redis_url="redis://localhost:6379",
)

# 2. 加载现有的向量库（注意这里直接初始化，不调用 from_documents）
vector_store = RedisVectorStore(embeddings_model, config=config)

# 3. 执行搜索
query = "我最近想换个手机"
# k=2 表示返回最相似的前 2 条结果
results = vector_store.similarity_search(query, k=2)

# 4. 查看结果
for doc in results:
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
    print("-" * 20)