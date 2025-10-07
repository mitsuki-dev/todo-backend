# app/security.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import hashlib

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ★ ここがポイント：truncate_error を False にする
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False,   # ← 追加
)

def _prehash(password: str) -> str:
    # 72バイト制限回避のため事前に固定長化
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(_prehash(password))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 順番は「平文, ハッシュ」
    return pwd_context.verify(_prehash(plain_password), hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
