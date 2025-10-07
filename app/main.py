# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ← 相対インポートにするのがポイント！
from .routes import auth, todos
from .database import Base, engine

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    docs_url="/docs",          # ← 明示的に指定
    redoc_url="/redoc",        # ← 任意。/redoc も見れるように
    openapi_url="/openapi.json"  # ← 明示的に指定（確認しやすい）
)

Base.metadata.create_all(bind=engine)


# CORS
# app/main.py の CORS 設定を差し替え
from fastapi.middleware.cors import CORSMiddleware

origins = [
    # ローカル
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://[::1]:3000",
    "http://192.168.11.3:3000",

    # 本番（Vercel）
    "https://todo-app-nu-wine.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                  # 明示リスト
    allow_origin_regex=r"https://.*\.vercel\.app",  # ← プレビュー含む *.vercel.app を許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録（今のままでOK。prefixは付けない方針のまま）
app.include_router(auth.router)
app.include_router(todos.router)

# ここを /status にしておくと確認が楽
@app.get("/status")
def status():
    return {"status": "ok"}