# backend/routers/templates.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Template
from schemas import BaseResponse, TemplateCreate, TemplateRead

router = APIRouter(prefix="/api/templates", tags=["templates"])

words=["{identity}","{genre}","{time}","{platform}","{topic}","{keyword}","{style}","{emotion}","{length}"]

def _validate_keyword(content: str):
    for word in words:
        if word not in content:
            return word
    return "ok"

@router.get("", response_model=BaseResponse)
def list_templates(db: Session = Depends(get_db)):
    items = db.query(Template).order_by(Template.create_time.desc()).all()
    data = [TemplateRead.model_validate(x) for x in items]  # pydantic v2
    return BaseResponse(code=200, msg="success", data=data)


@router.post("", response_model=BaseResponse)
def create_template(payload: TemplateCreate, db: Session = Depends(get_db)):
    if _validate_keyword(payload.content)!="ok":
        return BaseResponse(code=500, msg=f"模板 content 必须包含 {_validate_keyword(payload.content)}", data=None)

    obj = Template(
        name=payload.name.strip(),
        platform=payload.platform.strip(),
        content=payload.content,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return BaseResponse(code=200, msg="created", data=TemplateRead.model_validate(obj))


@router.put("/{template_id}", response_model=BaseResponse)
def update_template(template_id: int, payload: TemplateCreate, db: Session = Depends(get_db)):
    if _validate_keyword(payload.content)!="ok":
        return BaseResponse(code=500, msg=f"模板 content 必须包含 {_validate_keyword(payload.content)}", data=None)

    obj = db.query(Template).filter(Template.id == template_id).first()
    if not obj:
        return BaseResponse(code=500, msg=f"模板不存在: id={template_id}", data=None)

    obj.name = payload.name.strip()
    obj.platform = payload.platform.strip()
    obj.content = payload.content
    db.commit()
    db.refresh(obj)
    return BaseResponse(code=200, msg="updated", data=TemplateRead.model_validate(obj))


@router.delete("/{template_id}", response_model=BaseResponse)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    obj = db.query(Template).filter(Template.id == template_id).first()
    if not obj:
        return BaseResponse(code=500, msg=f"模板不存在: id={template_id}", data=None)

    db.delete(obj)
    db.commit()
    return BaseResponse(code=200, msg="deleted", data={"id": template_id})
