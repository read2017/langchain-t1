# uv add langchain_community unstructured[md]
from langchain_community.document_loaders import UnstructuredMarkdownLoader
import os
# 获取文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "assets", "sample.md")
docs = UnstructuredMarkdownLoader(
    # 文件路径
    file_path=file_path,
    # 加载模式:
    #   single 返回单个Document对象
    #   elements 按标题等元素切分文档
    mode="elements",
).load()

print(docs)