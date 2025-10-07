# app/routes/todos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, database
from app.routes.auth import get_current_user
from app.models import User  # 型ヒント用（必須ではないけどあると安心）

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=list[schemas.TodoRead])
def read_todos(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.list_todos(db) 


# タスク作成
@router.post("/", response_model=schemas.TodoRead)
def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    return crud.create_todo(db, current_user.id, todo)

# タスク更新
@router.put("/{task_id}", response_model=schemas.TodoRead)
def update_todo(
    task_id: int,
    todo: schemas.TodoUpdate,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    updated = crud.update_todo(db, task_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated


# タスク削除
@router.delete("/{task_id}")
def delete_todo(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    ok = crud.delete_todo(db, task_id)  # ← ここを修正（current_user.id を削除）
    if not ok:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "タスクが削除されました"}


@router.put("/{task_id}/toggle", response_model=schemas.TodoRead)
def toggle_task_complete(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(get_current_user),
):
    toggled = crud.toggle_todo(db, task_id, current_user.id)  # ← 3引数で呼ぶ
    if not toggled:
        raise HTTPException(status_code=404, detail="Todo not found")
    return toggled
