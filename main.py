from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Task
from schemas import TaskCreate, TaskResponse
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


def validate_task(task: Task):
    if task is None:
        raise HTTPException(status_code=404, detail="Value not found")


def get_task_by_id(id: int, database: Session):
    task = database.query(Task).filter(Task.id == id).first()
    validate_task(task)

    return task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(database: Session = Depends(get_database)):
    return database.query(Task).all()


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
def put_task(task_id: int, task_create: TaskCreate, database: Session = Depends(get_database)):
    task = get_task_by_id(task_id, database)
    task.text = task_create.text
    database.commit()
    database.refresh(task)
    return task
