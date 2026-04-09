"""
"placeholder" 是 ("placeholder", "{memory}") 的简写语法，
等价于 MessagesPlaceholder("memory")。

隐式使用MessagesPlaceholder
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

prompt = ChatPromptTemplate.from_messages([
    # 占位符，用于插入对话“记忆”内容，即之前的聊天记录（历史上下文）
    ("placeholder", "{memory}"),
    # 系统消息，用于设定 AI 的角色 —— 是一个资深的 Python 应用开发工程师
    ("system", "你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题"),
    # 用户当前提问，使用变量 {question} 进行动态填充
    ("human", "{question}")
])


# 使用 invoke 方法传入上下文变量，生成格式化后的对话 prompt 内容
formatted_prompt = prompt.invoke({
    "memory": [
        # 历史对话记录，包含系统消息、用户消息和 AI 消息
        SystemMessage(content="你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题"),
        HumanMessage(content="请问什么是Python？"),
        AIMessage(content="Python是一种高级编程语言，具有简洁易读的语法和丰富的库支持，广泛应用于数据分析、人工智能、Web开发等领域。")
    ],
    "question": "请问什么是Python的列表推导式？"
})

# 使用 .to_string() 将格式化后的对话链转换成纯文本字符串，方便查看输出
print(formatted_prompt.to_string())