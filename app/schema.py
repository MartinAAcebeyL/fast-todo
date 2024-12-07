import strawberry
from typing import List, Optional
from app.model import Task, tasks_db


@strawberry.type
class TaskType:
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False


@strawberry.type
class Query:
    @strawberry.field
    def tasks(self) -> List[TaskType]:
        return [
            TaskType(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
            )
            for task in tasks_db.values()
        ]

    @strawberry.field
    def task(self, id: int) -> Optional[TaskType]:
        task = tasks_db.get(id)
        return (
            TaskType(
                id=task.id,
                title=task.title,
                description=task.description,
                completed=task.completed,
            )
            if task
            else None
        )


@strawberry.input
class TaskInputType:
    title: str
    description: Optional[str] = None
    completed: bool = False


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(self, task: TaskInputType) -> TaskType:
        task_id = len(tasks_db) + 1
        new_task = Task(
            id=task_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )
        tasks_db[task_id] = new_task
        return TaskType(
            id=new_task.id,
            title=new_task.title,
            description=new_task.description,
            completed=new_task.completed,
        )

    @strawberry.mutation
    def update_task(self, id: int, task: TaskInputType) -> Optional[TaskType]:
        if id not in tasks_db:
            return None

        updated_task = Task(
            id=id,
            title=task.title,
            description=task.description,
            completed=task.completed,
        )
        tasks_db[id] = updated_task
        return TaskType(
            id=updated_task.id,
            title=updated_task.title,
            description=updated_task.description,
            completed=updated_task.completed,
        )

    @strawberry.mutation
    def delete_task(self, id: int) -> bool:
        if id not in tasks_db:
            return False

        del tasks_db[id]
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
