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
    keyword: str  # 用户输了什么词
