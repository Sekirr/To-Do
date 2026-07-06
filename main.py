from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, Task, Base, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks")
def get_tasks(db=Depends(get_db)):
    tasks = db.query(Task).all()
    db.close()
    return tasks


@app.post("/tasks")
def post_tasks(text_task: str, db=Depends(get_db)):
    task = Task(text=text_task)
    db.add(task)
    db.commit()
    db.refresh(task)
    db.close()
    return {"message": "Задача добавлена"}


@app.delete("/tasks")
def delete_tasks(id: int, db=Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    db.delete(task)
    db.commit()
    return {"message": "delete complete"}


@app.put("/tasks")
def put_task(id: int, new_value: str, db=Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    task.text = new_value
    db.commit()
    return {"message": "value update"}
