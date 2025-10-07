# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ← 相対インポートにするのがポイント！
from .routes import auth, todos
from .database import Base, engine

app = FastAPI()

# DBテーブル作成
Base.metadata.create_all(bind=engine)

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://[::1]:3000",        # 追加 (IPv6)
    "http://192.168.11.3:3000", # 追加 (自分のLAN IP, 必要なら)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # ← ここが正しい！
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ルーター登録
app.include_router(auth.router)
app.include_router(todos.router)
