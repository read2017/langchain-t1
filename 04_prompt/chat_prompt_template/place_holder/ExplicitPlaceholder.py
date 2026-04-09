"""
如果我们不确定消息何时生成，也不确定要插入几条消息，比如在提示词中添加聊天历史记忆这种场景，
可以在ChatPromptTemplate添加MessagesPlaceholder占位符，在调用invoke时，在占位符处插入消息。

显式使用MessagesPlaceholder
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 创建一个聊天提示模板，包含一个显式的消息占位符和系统、用户消息
# MessagesPlaceholder("memory") 定义了一个占位符，名称为 "memory"，用于插入对话历史记录
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("memory"),
    ("system", "你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题"),
    ("human", "{question}")
])

# 使用 invoke 方法传入上下文变量，生成格式化后的对话 prompt 内容
formatted_prompt = prompt.invoke({
    "memory": [
        SystemMessage(content="你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题"),
        HumanMessage(content="请问什么是Python？"),
        AIMessage(content="Python是一种高级编程语言，具有简洁易读的语法和丰富的库支持，广泛应用于数据分析、人工智能、Web开发等领域。")
    ],
    "question": "请问什么是Python的列表推导式？"
})

# 使用 .to_string() 将格式化后的对话链转换成纯文本字符串，方便查看输出
print(formatted_prompt.to_string())