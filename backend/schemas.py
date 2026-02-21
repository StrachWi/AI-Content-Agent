from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


# --- 1. 统一响应格式 (后端不管成功失败，都回这个) ---
class BaseResponse(BaseModel):
    code: int = 200  # 状态码：200成功，500错误
    msg: str = "success"  # 提示信息
    data: Optional[Any] = None  # 真正的数据


# --- 2. 给素材组用的模型 (前端传来的数据样子) ---
class TemplateCreate(BaseModel):
    name: str
    platform: str
    content: str  # 必须包含 {keyword} 占位符


class TemplateRead(TemplateCreate):
    id: int
    create_time: datetime

    class Config:
        from_attributes = True


# --- 3. 给AI组用的模型 (前端传来的生成请求) ---
class GenerateRequest(BaseModel):
    template_id: int  # 用户选了哪个模板
    identity: str  # 用户的身份，例如学生、博主等等
    genre: str  # 用户想要的文体，例如正式、幽默等等
    time: str  # 用户想要的时间，例如现在、昨天等等
    platform: str  # 用户想要的发布平台，例如小红书、抖音等等
    topic: str  # 用户想要的主题，例如美食等等
    keyword: str  # 用户输了什么关键词
    style: str  # 用户想要的风格，例如文艺、搞笑等等
    emotion: str  # 用户想要的情绪，例如开心、伤感等等
    length: str  # 用户想要的长度，例如短、中、长、或者精确到多少字以内等等