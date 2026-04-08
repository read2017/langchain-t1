# 方式2：外部加载Prompt,将 prompt 保存为 yaml
from langchain_core.prompts import load_prompt
import os
# 获取当前目录下的prompt.yaml文件
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(current_dir, "prompt.yaml")
print(prompt_path)
template = load_prompt(prompt_path, encoding="utf-8")
print(template.format(name="年轻人", what="滑稽"))
# 请年轻人讲一个滑稽的故事