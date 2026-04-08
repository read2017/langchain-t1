from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen3.5", reasoning=False)

print(model.invoke("什么是Langchain?").content)