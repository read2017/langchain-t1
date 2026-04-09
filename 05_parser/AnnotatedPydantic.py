from typing import Annotated
from pydantic import BaseModel, Field, ValidationError

Age = Annotated[int, Field(..., ge=0, le=150, description="年龄，范围0-150")]

class Person(BaseModel):
    name: str
    age1: int
    age2: Age

try:
    p = Person(name="Alice", age1="30", age2=25)
    print(p)
except ValidationError as e:
    print("验证错误：", e)