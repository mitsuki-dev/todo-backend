# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from app import schemas, crud, security
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

# Swagger の Authorize 用（tokenUrl は /auth/login に合わせるだけ。実際の取得はJSONでOK）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ===== サインアップ（カリキュラム仕様） =====
@router.post("/signup", response_model=schemas.Message)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.create_user(db=db, user=user)
    return {"message": "アカウントが作成されました"}

# ===== ログイン（カリキュラム仕様：JSON受け取りでトークン返す） =====
@router.post("/login", response_model=schemas.Token)
def login(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = security.create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 互換: 既存の /auth/token も同じ挙動で残す
@router.post("/token", response_model=schemas.Token)
def token_alias(user: schemas.LoginRequest, db: Session = Depends(get_db)):
    return login(user, db)

# ===== 認証ユーザー取得（任意・確認用） =====
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    cred_err = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise cred_err
    except JWTError:
        raise cred_err

    user = crud.get_user_by_username(db, username)
    if user is None:
        raise cred_err
    return user

@router.get("/me", response_model=schemas.UserRead)
def read_me(current_user=Depends(get_current_user)):
    return current_user
