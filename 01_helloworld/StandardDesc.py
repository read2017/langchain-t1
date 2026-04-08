from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_core.exceptions import LangChainException

load_dotenv(encoding='utf-8')

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def init_llm_client() -> ChatOpenAI:
    try:
        my_key = os.getenv("DASHSCOPE_API_KEY")
        if not my_key:
            raise ValueError("DASHSCOPE_API_KEY is not set in environment variables.")
        
        llm_client = ChatOpenAI(
            model="qwen-plus",
            # model_provider="openai",
            api_key=my_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        logger.info("LLM client initialized successfully.")
        return llm_client
    except Exception as e:
        logger.error(f"Failed to initialize LLM client: {e}")
        raise LangChainException(f"LLM client initialization error: {e}")
    
if __name__ == "__main__":
    llm_client = init_llm_client()
    question = "Hello, world!"
    response = llm_client.invoke(question)
    logger.info(f"问题：{question}")
    logger.info(f"回答：{response.content}")
    print(response.content)

    print("测试流式输出：=============================")
    for chunk in llm_client.stream(question):
        # logger.info(f"流式输出：{chunk.content}")
        print(chunk.content, end='', flush=True)