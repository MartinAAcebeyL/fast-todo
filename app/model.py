from typing import Dict, Optional
from pydantic import BaseModel, Field
import strawberry

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    completed: bool = False


class Task(TaskCreate):
    id: int


tasks_db: Dict[int, Task] = {}
