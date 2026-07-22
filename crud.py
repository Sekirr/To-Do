from database import Task
from schemas import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_task_by_id(id: int, database: Session):
    task = database.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Value not found")

    return task


def create_task(task_create: TaskCreate,	database: Session):
    task = Task(text=task_create.text)
    database.add(task)
    database.commit()
    database.refresh(task)
    return task


def delete_task(task_id: int, database: Session):
    task = get_task_by_id(task_id, database)
    database.delete(task)
    database.commit()
    return {"message": "delete complete"}


def update_task(task_id: int, task_update: TaskUpdate, database: Session):
    task = get_task_by_id(task_id, database)
    task.text = task_update.text
    task.completed = task_update.completed
    database.commit()
    database.refresh(task)
    return task


def toggle_task_completion(task_id: int, database: Session):
    task = get_task_by_id(task_id, database)
    task.completed = not task.completed
    database.commit()
    database.refresh(task)
    return task
