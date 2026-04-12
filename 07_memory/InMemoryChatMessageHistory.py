from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
import os
from loguru import logger

llm = init_chat_model(
    model = "qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 创建一个InMemoryChatMessageHistory对象来存储聊天历史
chat_history = InMemoryChatMessageHistory()
# 向聊天历史中添加一些消息，模拟之前的对话内容
chat_history.add_user_message("你好，AI助手！我叫张三，我的爱好是学习")

ai_message = llm.invoke(chat_history.messages)
logger.info(f"AI助手的回复：{ai_message}")

# 将AI回复添加到聊天历史记录中
chat_history.add_ai_message(ai_message.content)
logger.info(f"当前聊天历史：{chat_history.messages}")

# 添加新的用户消息到聊天历史记录
chat_history.add_user_message("我叫什么？我的爱好是什么？")
logger.info(f"更新后的聊天历史：{chat_history.messages}")

# 再次调用模型，传入更新后的聊天历史记录，获取AI的回复
ai_message2 = llm.invoke(chat_history.messages)
logger.info(f"AI助手的回复：{ai_message2}")

# 遍历并输出所有聊天历史记录中的消息内容
# for idx, message in enumerate(chat_history.messages):
#     logger.info(f"消息 {idx + 1}: {message.content}")

for message in chat_history.messages:
    logger.info(message.content)