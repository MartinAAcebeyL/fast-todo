from fastapi import APIRouter, HTTPException
from typing import List
from app.model import Task, TaskCreate, tasks_db

router = APIRouter()


@router.get("/", response_model=List[Task])
async def list_tasks():
    return list(tasks_db.values())


@router.post("/", response_model=Task)
async def create_task(task: TaskCreate):
    task_id = len(tasks_db) + 1
    new_task = Task(id=task_id, **task.dict())
    tasks_db[task_id] = new_task
    return new_task


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: TaskCreate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    task = Task(id=task_id, **updated_task.dict())
    tasks_db[task_id] = task
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks_db[task_id]
