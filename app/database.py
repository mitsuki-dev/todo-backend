from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite用のDB URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo_app.db"

# DBエンジン作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデル作成時に継承するベースクラス
Base = declarative_base()


# DBセッションを取得する関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        