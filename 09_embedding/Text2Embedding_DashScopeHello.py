import dashscope  
from http import HTTPStatus
# https://bailian.console.aliyun.com/cn-beijing/?productCode=p_efm&tab=doc#/doc/?type=model&url=2842587
input_text = "衣服的质量很好"

resp = dashscope.TextEmbedding.call(
    model="text-embedding-v4",
    input=input_text
)

if resp.status_code == HTTPStatus.OK:
    print(resp)