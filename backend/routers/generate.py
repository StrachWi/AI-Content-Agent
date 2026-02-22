# backend/routers/generate.py
import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Template, History
from schemas import BaseResponse, GenerateRequest

router = APIRouter(prefix="/api/generate", tags=["AI生成"])

# 这里填写你的 AI 密钥和接口地址（以 DeepSeek 为例，OpenAI 同理）
API_KEY = "你的API_KEY"
BASE_URL = "https://api.deepseek.com/chat/completions" 

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
                    "model": "deepseek-chat", # 或 gpt-3.5-turbo
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
