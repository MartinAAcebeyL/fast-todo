from fastapi import FastAPI
from app.routes import router as tasks_router
from strawberry.fastapi import GraphQLRouter
from app.schema import schema

app = FastAPI(title="Todo API", description="Simple Task Management API")
graphql_router = GraphQLRouter(schema)

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(graphql_router, prefix="/graphql")
