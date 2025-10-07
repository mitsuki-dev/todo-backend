# app/crud.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas
from app.security import get_password_hash

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# ===== Users =====
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

# ===== Todos =====
def create_todo(db: Session, user_id: int, todo_in: schemas.TodoCreate) -> models.Todo:
    todo = models.Todo(
        title=todo_in.title,
        details=todo_in.details,
        completed=todo_in.completed,
        user_id=user_id,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def list_todos(db: Session, skip: int = 0, limit: int = 100) -> List[models.Todo]:
    return db.query(models.Todo).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int) -> Optional[models.Todo]:
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def update_todo(db: Session, todo_id: int, todo_in: schemas.TodoUpdate) -> Optional[models.Todo]:
    todo = get_todo(db, todo_id)
    if not todo:
        return None
    if todo_in.title is not None:
        todo.title = todo_in.title
    if todo_in.details is not None:
        todo.details = todo_in.details
    if todo_in.completed is not None:
        todo.completed = todo_in.completed
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int) -> bool:
    todo = get_todo(db, todo_id)
    if not todo:
        return False
    db.delete(todo)
    db.commit()
    return True

def toggle_todo(db: Session, todo_id: int, user_id: int) -> Optional[models.Todo]:
    # 自分のタスクだけを対象にする
    todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.user_id == user_id
    ).first()

    if not todo:
        return None

    # 完了フラグを反転
    todo.completed = not todo.completed
    db.commit()
    db.refresh(todo)
    return todo