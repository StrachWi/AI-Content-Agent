# backend/routers/generate.py
import httpx
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Template, History
from schemas import BaseResponse, GenerateRequest

router = APIRouter(prefix="/api/generate", tags=["AI生成"])


# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取配置
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("API_BASE_URL", "https://api.deepseek.com")

# 如果 API_KEY 未设置，提供一个更明确的错误
if not API_KEY:
    print("警告: 未正确配置 DEEPSEEK_API_KEY，请检查 .env 文件")

@router.post("", response_model=BaseResponse)
async def generate_content(payload: GenerateRequest, db: Session = Depends(get_db)):
    # 1. 获取模板
    template = db.query(Template).filter(Template.id == payload.template_id).first()
    if not template:
        return BaseResponse(code=500, msg="模板不存在", data=None)

    # 2. 拼接 Prompt (把 9 大占位符替换成用户的输入)
    # 使用 .format(**dict) 自动匹配字符串中的 {keyword} 等
    try:
        prompt = template.content.format(
            identity=payload.identity,
            genre=payload.genre,
            time=payload.time,
            platform=payload.platform,
            topic=payload.topic,
            keyword=payload.keyword,
            style=payload.style,
            emotion=payload.emotion,
            length=payload.length
        )
    except KeyError as e:
        return BaseResponse(code=500, msg=f"模板参数匹配失败: 缺少 {e}", data=None)

    # 3. 调用 AI 接口
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                BASE_URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={
                    "model": "deepseek-chat", 
                    "messages": [
                        {"role": "system", "content": "你是一个自媒体文案专家。"},
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=60.0
            )
            res_json = response.json()
            ai_text = res_json["choices"][0]["message"]["content"]
    except Exception as e:
        return BaseResponse(code=500, msg=f"AI 接口调用失败: {str(e)}", data=None)

    # 4. 自动保存到历史记录 (为第4组提供数据)
    new_history = History(
        template_id=template.id,
        user_input=payload.keyword,
        ai_result=ai_text
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    return BaseResponse(code=200, msg="生成成功", data={"result": ai_text, "history_id": new_history.id})
