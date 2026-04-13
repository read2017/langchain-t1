from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputKeyToolsParser, StrOutputParser
from QueryWeaterTool import get_weather
from loguru import logger
import os

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 将模型与工具绑定，使其能够调用 get_weather 工具
llm_with_tools = llm.bind_tools([get_weather])


# 创建解析器，用于提取工具调用结果中的 JSON 数据
parser = JsonOutputKeyToolsParser(key_name = get_weather.name, first_tool_only=True)

# 构建工具调用链 
get_weather_chain = llm_with_tools | parser | get_weather
# print("get_weather_chain:", get_weather_chain.invoke("你好， 请问北京的天气怎么样？")) 
# get_weather_chain: 查询天气失败，错误代码：404，错误信息：{"cod":"404","message":"city not found"}
# 定义输出提示模板，将 JSON 天气数据转换为自然语言描述
output_prompt = PromptTemplate.from_template(
    """你将收到一段 JSON 格式的天气数据{weather_json}，请用简洁自然的方式将其转述给用户。
    以下是天气 JSON 数据：
    请将其转换为中文天气描述，例如：
    “北京现在天气：多云，气温 28℃，体感有点闷热（约 32℃），湿度 75%，微风（东南风 2 米/秒），
    能见度很好，大约 10 公里。建议穿短袖短裤。适合做户外运动。"
    """
)
output_parser = StrOutputParser()
output_chain = output_prompt | llm | output_parser

full_chain = get_weather_chain | (lambda x:{"weather_json": x}) | output_chain


# 执行完整链路，查询上海天气并打印结果
result = full_chain.invoke("请问北京(Beijing)今天的天气如何？")
logger.info(result)