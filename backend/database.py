from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库文件名为 sql_app.db，就在当前目录下
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 创建引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类，用于创建模型
Base = declarative_base()


# 依赖项：每个接口调用时获取数据库会话，调用完自动关闭
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
