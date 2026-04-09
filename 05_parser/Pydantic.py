"""
PydanticOutputParser 是 LangChain 输出解析器体系中最常用、最强大的结构化解析器之一。
它与 JsonOutputParser 类似，但功能更强 —— 能直接基于 Pydantic 模型 定义输出结构，
并利用其类型校验与自动文档能力。
对于结构更复杂、具有强类型约束的需求，PydanticOutputParser 则是最佳选择。
它结合了Pydantic模型的强大功能，提供了类型验证、数据转换等高级功能
"""
import os
from pydantic import BaseModel, Field, field_validator
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

# 定义Pydantic模型，描述输出数据的结构和类型
class Product(BaseModel):
    """
    产品信息模型类，用于定义产品的结构化数据格式

    属性:
        name (str): 产品名称
        category (str): 产品类别
        description (str): 产品简介，长度必须大于等于10个字符
    """
    name: str = Field(..., description="产品名称")
    category: str = Field(..., description="产品类别")
    description: str = Field(..., description="产品简介，长度必须大于等于10个字符")

    @field_validator("description")
    def validate_description(cls, value):
        if len(value) < 10:
            raise ValueError("产品简介必须至少包含10个字符")
        return value

#  创建Pydantic输出解析器实例，用于解析模型输出为Product对象
parser = PydanticOutputParser(pydantic_object=Product)
# 获取格式化指令，指导模型生成符合Product结构的输出
format_instructions = parser.get_format_instructions()

# 创建聊天提示模板，包含系统角色设定和用户问题输入
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请简短回答我提出的问题，结果返回json格式，必须符合以下格式要求：{format_instructions}"),
    ("user", "请你输出标题为：{topic}的新闻内容")
])
# 格式化提示消息，填充主题和格式化指令
formatted_prompt = prompt.format_messages(
    role="新闻生成器",
    topic="人工智能的最新发展",
    format_instructions=format_instructions
)
logger.info(f"生成的提示词：{formatted_prompt}")
# 初始化聊天模型，这里使用了一个名为"qwen-plus"的模型，提供者是OpenAI，API密钥从环境变量中获取，base_url指定了模型的访问地址
model = init_chat_model(
    model = "qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
# 发送提示词给模型并获取响应
response = model.invoke(formatted_prompt)
logger.info(f"模型返回的原始响应：{response}")
# 打印类型
print("原始响应的类型：", type(response))