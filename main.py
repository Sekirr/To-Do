from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Task
from schemas import TaskCreate, TaskResponse, TaskUpdate
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_task_by_id(id: int, database: Session):
    task = database.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Value not found")

    return task


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, database: Session = Depends(get_database)):
    task = get_task_by_id(task_id, database)
    return task


@app.get("/tasks", response_model=list[TaskResponse])
def task_completed(
        completed: bool | None = Query(default=False),
        limit: int | None = Query(default=5),
        offset: int | None = Query(default=0),
        database: Session = Depends(get_database)):
    task = database.query(Task).filter(
        Task.completed == completed).offset(offset).limit(limit).all()
    return task


@app.post("/tasks", response_model=TaskResponse)
def post_tasks(task_create: TaskCreate, database: Session = Depends(get_database)):
    task = Task(text=task_create.text)
    database.add(task)
    database.commit()
    database.refresh(task)
    return task


@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_tasks(task_id: int, database: Session = Depends(get_database)):
    task = get_task_by_id(task_id, database)
    database.delete(task)
    database.commit()
    return {"message": "delete complete"}


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def put_task(task_id: int, task_update: TaskUpdate, database: Session = Depends(get_database)):
    task = get_task_by_id(task_id, database)
    task.text = task_update.text
    task.completed = task_update.completed
    database.commit()
    database.refresh(task)
    return task


@app.patch("/tasks/{task_id}/toggle", response_model=TaskResponse)
def patch_task(task_id: int, database: Session = Depends(get_database)):
    task = get_task_by_id(task_id, database)
    task.completed = not task.completed
    database.commit()
    database.refresh(task)
    return task
