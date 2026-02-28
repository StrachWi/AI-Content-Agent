from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, and_, or_
from datetime import datetime, timedelta
from typing import Optional

from database import get_db
from models import History
from schemas import BaseResponse, HistoryCreate, HistoryRead, StatsData

router = APIRouter(prefix="/api", tags=["历史记录与统计"])


@router.post("/history", response_model=BaseResponse)
async def create_history(payload: HistoryCreate, db: Session = Depends(get_db)):
    try:
        new_history = History(
            topic=payload.topic,
            platform=payload.platform,
            ai_result=payload.content,
            template_name=payload.template_name,
            user_input=payload.topic
        )
        db.add(new_history)
        db.commit()
        db.refresh(new_history)
        
        return BaseResponse(code=200, msg="保存成功", data={"id": new_history.id})
    except Exception as e:
        db.rollback()
        return BaseResponse(code=500, msg=f"保存失败: {str(e)}", data=None)


@router.get("/history", response_model=BaseResponse)
async def get_histories(
    keyword: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(History)
        
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.filter(
                or_(
                    History.topic.like(search_pattern),
                    History.ai_result.like(search_pattern),
                    History.platform.like(search_pattern)
                )
            )
        
        total = query.count()
        histories = query.order_by(History.create_time.desc()).offset((page - 1) * limit).limit(limit).all()
        
        result_list = []
        for h in histories:
            result_list.append({
                "id": h.id,
                "topic": h.topic or "",
                "time": h.create_time.strftime("%Y-%m-%d %H:%M") if h.create_time else "",
                "platform": h.platform or "",
                "content": h.ai_result or "",
                "template_name": h.template_name or ""
            })
        
        return BaseResponse(
            code=200, 
            msg="success", 
            data={
                "list": result_list,
                "total": total,
                "page": page,
                "limit": limit
            }
        )
    except Exception as e:
        return BaseResponse(code=500, msg=f"查询失败: {str(e)}", data=None)


@router.delete("/history/{history_id}", response_model=BaseResponse)
async def delete_history(history_id: int, db: Session = Depends(get_db)):
    try:
        history = db.query(History).filter(History.id == history_id).first()
        if not history:
            return BaseResponse(code=404, msg="记录不存在", data=None)
        
        db.delete(history)
        db.commit()
        
        return BaseResponse(code=200, msg="删除成功", data=None)
    except Exception as e:
        db.rollback()
        return BaseResponse(code=500, msg=f"删除失败: {str(e)}", data=None)


@router.get("/stats", response_model=BaseResponse)
async def get_stats(db: Session = Depends(get_db)):
    try:
        today = datetime.now().date()
        
        total = db.query(func.count(History.id)).scalar()
        
        today_count = db.query(func.count(History.id)).filter(
            func.date(History.create_time) == today
        ).scalar()
        
        hot_template_result = db.query(
            History.template_name,
            func.count(History.id).label('count')
        ).filter(
            History.template_name.isnot(None)
        ).group_by(
            History.template_name
        ).order_by(
            func.count(History.id).desc()
        ).first()
        
        hot_template = hot_template_result[0] if hot_template_result else "暂无数据"
        
        chart_data = []
        for i in range(7):
            date = today - timedelta(days=6-i)
            count = db.query(func.count(History.id)).filter(
                func.date(History.create_time) == date
            ).scalar()
            chart_data.append(count if count else 0)
        
        stats_data = {
            "total": total if total else 0,
            "today": today_count if today_count else 0,
            "hotTemplate": hot_template,
            "chartData": chart_data
        }
        
        return BaseResponse(code=200, msg="success", data=stats_data)
    except Exception as e:
        return BaseResponse(code=500, msg=f"统计失败: {str(e)}", data=None)