from langchain_community.document_loaders import TextLoader
import os
# 获取文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "assets", "sample.txt")
# 加载文件
docs = TextLoader(file_path).load()
print(docs)
# [Document(metadata={'source': 'asset/sample.txt'}, page_content='...')]