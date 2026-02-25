from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers.templates import router as templates_router
from routers import generate
# --- 核心动作：创建数据库表 ---
# 这一步非常关键！它会根据 models.py 自动生成 sql_app.db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 配置 (保持你之前的配置不变)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "AI 营销助手后端已启动！数据库连接正常。"}


# 以后大家写的路由(Router)会在这里引入
app.include_router(templates_router)
app.include_router(generate.router)
