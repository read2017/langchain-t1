from langchain_community.document_loaders import PyPDFLoader
import os
# 获取文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "assets", "sample.pdf")
# 加载文件
docs = PyPDFLoader(
    file_path=file_path,
    # 提取模式:
    #   plain 提取文本
    #   layout 按布局提取
    extraction_mode="plain",
).load()
print(docs)