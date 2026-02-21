from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


# --- 表1：素材/模板表 (2组负责维护，3组负责读取) ---
class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # 模板名称，如"小红书种草"
    platform = Column(String(50))  # 适用平台，如"小红书"、"抖音"

    # 核心字段：这是2组设计的带"钉子"的模具
    # 例如："你是一个博主...请根据关键词 {keyword} 写文案..."
    content = Column(Text, nullable=False)

    create_time = Column(DateTime(timezone=True), server_default=func.now())


# --- 表2：创作历史表 (3组负责写入，4组负责读取) ---
class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True, index=True)

    # 记录用了哪个模板生成的
    template_id = Column(Integer, nullable=True)

    # 用户当时输入的关键词 (为了方便回顾)
    user_input = Column(Text)

    # AI 生成的结果 (存下来，防止丢失)
    ai_result = Column(Text)

    create_time = Column(DateTime(timezone=True), server_default=func.now())
