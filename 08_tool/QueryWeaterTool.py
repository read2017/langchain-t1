from langchain.tools import tool
import os
import json
import httpx

# 打印天气API Key
# print(f"WEATHER_API_KEY = {os.getenv('WEATHER_API_KEY')}")

@tool(name_or_callable="get_weather", description="查询指定城市的天气信息", return_direct=True)
def get_weather(loc: str) -> str:
    """
    查询即时天气函数

    :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称。
                注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京/上海市天气，
                则 loc 参数需要输入 'Beijing'/'shanghai'。
    :return: OpenWeather API 查询即时天气的结果。具体 URL 请求地址为：
             https://home.openweathermap.org/users/sign_in。
             返回结果对象类型为解析之后的 JSON 格式对象，并用字符串形式进行表示，
             其中包含了全部重要的天气信息。
    """
    # Step 1. 构建请求 URL
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Step 2. 设置查询参数，包括城市名、API Key、单位和语言
    params = {
        "q": loc,
        "appid": os.getenv("WEATHER_API_KEY"),  # 从环境变量中读取 API Key
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn"  # 输出语言为简体中文
    }

    # Step 3. 发送 GET 请求并获取响应
    response = httpx.get(url, params=params, timeout=20)

    # Step 4. 解析响应 JSON 数据
    if response.status_code == 200:
        data = response.json()
        # 提取天气信息并格式化输出
        # weather_info = {
        #     "城市": data.get("name"),
        #     "天气": data["weather"][0]["description"],
        #     "温度": f"{data['main']['temp']}°C",
        #     "湿度": f"{data['main']['humidity']}%",
        #     "风速": f"{data['wind']['speed']} m/s"
        # }
        # return json.dumps(weather_info, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)
    else:
        return f"查询天气失败，错误代码：{response.status_code}，错误信息：{response.text}"

# 测试
# result = get_weather.invoke("shanghai")
# result = get_weather.invoke("beijing")
# print(result)