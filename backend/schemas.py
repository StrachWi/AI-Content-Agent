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


# --- 3. 给AI组用的模型 (升级版：包含9大钉子) ---
class GenerateRequest(BaseModel):
    template_id: int  # 模板编号

    # --- 核心 9 大参数 (设为可选，给定默认值，防止报错) ---
    keyword: str  # 关键词

    identity: Optional[str] = "资深文案专家"  # 身份
    genre: Optional[str] = "社交媒体文案"  # 体裁
    time: Optional[str] = "近期"  # 时间
    platform: Optional[str] = "全网"  # 平台
    topic: Optional[str] = "通用"  # 主题
    style: Optional[str] = "吸引人"  # 风格
    emotion: Optional[str] = "积极"  # 情感
    length: Optional[str] = "200字左右"  # 字数


# --- 4. 给历史记录组用的模型 ---
class HistoryCreate(BaseModel):
    topic: str  # 创作主题
    platform: str  # 发布平台
    content: str  # AI生成内容
    template_name: str  # 使用模板名称


class HistoryRead(BaseModel):
    id: int
    topic: str
    time: str  # 格式为 YYYY-MM-DD HH:mm
    platform: str
    content: str

    class Config:
        from_attributes = True


# --- 5. 统计数据模型 ---
class StatsData(BaseModel):
    total: int  # 总记录数
    today: int  # 今日生成数
    hotTemplate: str  # 使用次数最多的模板名称
    chartData: list[int]  # 近 7 天每日生成数量数组
