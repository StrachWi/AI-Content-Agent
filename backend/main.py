from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORS (解决跨域问题，否则前端访问不了后端)
origins = [
    "http://localhost:5173",  # Vue 默认端口
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
    return {"message": "后端服务运行成功！Hello from FastAPI"}


@app.get("/api/test")
def test_api():
    return {"data": "这是从后端获取的数据"}
