# pip install langchain_community unstructured[docx]
# uv add unstructured
# pip install python-docx
# pip install regex==2026.1.14

from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import os
from langchain_community.document_loaders import Docx2txtLoader
# 获取文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "assets", "sample.docx")
# 加载文件
# docs = UnstructuredWordDocumentLoader(file_path).load()
loader = Docx2txtLoader(file_path)
docs = loader.load()
# 打印docs的类型
print('docs的类型：', type(docs))

# 打印docs的内容
# print('docs的内容：', docs)