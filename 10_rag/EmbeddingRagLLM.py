# pip install unstructured
# pip install docx2txt
# pip install python-docx
from langchain.chat_models  import  init_chat_model
import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.prompts import PromptTemplate
from langchain_classic.text_splitter import CharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis

# 没有使用RAG，直接查询大模型，出现歧义，上课时先给学生演示before情况，没有用RAG
'''llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
response=llm.invoke("00000是什么意思")
print(response.content)'''

# 获取文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "alibaba-java.docx")

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

prompt_template = """
    请使用以下提供的文本内容来回答问题。仅使用提供的文本信息，
    如果文本中没有相关信息，请回答"抱歉，提供的文本中没有这个信息"。

    文本内容：
    {context}

    问题：{question}

    回答：
    "
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# 1. 初始化阿里千问 Embedding 模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",  # 支持 v1 或 v2
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")  # 从环境变量读取
)

# 4. 加载文档
# 4.1 TextLoader 无法处理 .docx 格式文件，专门用于加载纯文本文件的（如 .txt）
# loader = TextLoader("alibaba-more.docx", encoding="utf-8")

# 4.2 LangChain提供了Docx2txtLoader专门用于加载.docx文件，先通过pip install docx2txt
loader = Docx2txtLoader(file_path)  # 直接传入文件路径即可
documents = loader.load()

# 5. 分割文档
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function=len)
texts = text_splitter.split_documents(documents)

print(f"文档个数:{len(texts)}")

# 6. 创建向量存储
# 连接到 Redis 并存入向量（自动调用 embeddings 嵌入）
vector_store = Redis.from_documents(
    documents=documents,
    embedding=embeddings,
    redis_url="redis://localhost:6379",  # 替换为你的 Redis 地址
    index_name="alibaba_status_code",  # 向量索引名称
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 8. 创建Runnable链
rag_chain = (
        {
            "context": retriever, # 这一行负责去 Redis 搜相关的“辅导书内容”
            "question": RunnablePassthrough() # 这一行负责把用户的原问题直接“传球”给下一步
        }
        | prompt
        | llm
)

# 9. 提问
question = "00000和A0001分别是什么意思"
result = rag_chain.invoke(question)
print("\n问题:", question)
print("\n回答:", result.content)

'''
这行代码看似简单，实际上它是连接“静态数据库”与“动态大模型”的**枢纽**。我们可以从底层逻辑、数据类型和参数传递机制三个维度来拆解。

### 1. `retriever` 到底是什么？

* **它不是函数，是一个对象（Object）**。
* **具体类型**：它是 LangChain 中的 `VectorStoreRetriever` 类的一个实例。
* **本质**：它是一个**“包装器”**。它把复杂的向量数据库操作封装成了一个简单的接口。你只需要给它一个字符串（问题），它就能返回相关的 `Document` 列表。

### 2. `as_retriever` 做了什么？

`vector_store` 是一个存满数据的数据库，它有很多底层操作（比如增加数据、删除索引、原始搜索等）。
当你执行 `as_retriever()` 时，你实际上是在说：**“我不需要操作数据库的所有功能，请给我一个专门负责‘根据问题找答案’的精简版工具。”**

这就好比：`vector_store` 是**整个图书馆**，而 `retriever` 是你雇佣的一个**图书管理员**。

---

### 3. 参数 `search_kwargs={"k": 2}` 是怎么传递的？

这里最让人困惑的是：**参数传给谁了？什么时候生效？**

#### A. 传递路径
当你写 `{"k": 2}` 时，这个参数并没有立即执行搜索。它被存放在 `retriever` 对象的**内部属性**中。
* **存储位置**：`retriever.search_kwargs`。
* **作用对象**：它最终是传给 Redis 的 `similarity_search` 函数的。

#### B. 内部逻辑拆解
当你后续调用 `rag_chain.invoke(question)` 时，发生了以下连锁反应：
1.  **触发**：Chain 运行到 `retriever` 这一步。
2.  **调用**：Chain 自动调用 `retriever.get_relevant_documents(question)`。
3.  **合并**：`retriever` 内部会把 `question` 和它兜里揣着的 `{"k": 2}` 合并。
4.  **执行**：最终去执行类似 `vector_store.similarity_search(question, k=2)` 的动作。



---

### 4. 为什么要这样设计？（解惑：哪里传的参数）

你可能会问：**“我调用 invoke 时只传了 question，没传 k 啊？”**

这就是 LangChain **“声明式编程”** 的核心思想：
* **配置阶段**（这就是你问的那行代码）：提前定义好这个管理员的“工作习惯”（比如：每次必须找回 2 条数据，不要多也不要少）。
* **执行阶段**（`invoke`）：你只需要下达任务（提问），不需要再关心搜索细节。

### 5. 常见的 `search_kwargs` 还能传什么？

除了 `k`（返回几个结果），你还可以传递：
* **`score_threshold`**：相似度阈值。比如只找相似度大于 0.8 的内容。
* **`filter`**：元数据过滤。比如 `{"filter": {"category": "水果"}}`。
* **`search_type`**：搜索类型。除了默认的 `similarity`（相似度），还可以设为 `mmr`（最大边界相关性，用来保证找回的几条结果之间不重复）。

### 总结
* **类型**：`VectorStoreRetriever` 对象。
* **传参方式**：在**初始化阶段**通过字典（Dictionary）预设参数。
* **生效时机**：在 `chain.invoke()` 被调用时，由 Chain 自动将问题和预设参数组合后去查询数据库。

你可以理解为：这行代码是在给图书管理员下**岗前培训指令**，告诉他以后不论谁来问问题，都只准找回最相关的 2 本书。
'''