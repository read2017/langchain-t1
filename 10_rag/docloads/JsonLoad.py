from langchain_community.document_loaders import JSONLoader
import os
import json
# 获取文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "assets", "sample.json")
# 读取并打印json文件内容
with open(file_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
print(json.dumps(json_data, indent=4, ensure_ascii=False))
# 提取所有字段
docs = JSONLoader(
    file_path=file_path,
    jq_schema='.',
    text_content=False
).load()
print(docs)
