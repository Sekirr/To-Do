from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Task, Base, engine
from schemas import TaskCreate

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


def check_connection(task):
    if task is None:
        raise HTTPException(status_code=404, detail="Value not found")


def get_task_by_id(id: int, database):
    task = database.query(Task).filter(Task.id == id).first()
    check_connection(task)

    return task


@app.get("/tasks")
def get_tasks(database=Depends(get_database)):
    return database.query(Task).all()


@app.post("/tasks")
def post_tasks(task_create: TaskCreate, database=Depends(get_database)):
    if not task_create.text.strip():
        raise HTTPException(status_code=404, detail="Data text uncorrected.")

    task = Task(text=task_create.text)
    database.add(task)
    database.commit()
    database.refresh(task)
    return {"message": "Task created complete"}


@app.delete("/tasks")
def delete_tasks(id: int, database=Depends(get_database)):
    task = get_task_by_id(id, database)
    database.delete(task)
    database.commit()
    return {"message": "delete complete"}


@app.put("/tasks")
def put_task(id: int, new_value: str, database=Depends(get_database)):
    task = get_task_by_id(id, database)
    task.text = new_value
    database.commit()
    return {"message": "value update"}
