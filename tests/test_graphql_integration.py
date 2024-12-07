# tests/test_graphql_integration.py
from fastapi.testclient import TestClient
from app.main import app
from app.model import tasks_db

client = TestClient(app)


def setup_function():
    """Limpiar la base de datos antes de cada prueba"""
    tasks_db.clear()


def test_create_task_mutation():
    """Prueba mutación de creación de tarea en GraphQL"""
    query = """
    mutation {
        createTask(task: {
            title: "GraphQL Test Task", 
            description: "GraphQL Test Description"
        }) {
            id
            title
            description
            completed
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200

    data = response.json()
    created_task = data["data"]["createTask"]

    assert created_task["title"] == "GraphQL Test Task"
    assert created_task["description"] == "GraphQL Test Description"
    assert created_task["completed"] == False


def test_update_task_mutation():
    """Prueba mutación de actualización de tarea en GraphQL"""
    # Primero crear una tarea
    create_query = """
    mutation {
        createTask(task: {title: "Task to Update"}) {
            id
        }
    }
    """
    create_response = client.post("/graphql", json={"query": create_query})
    task_id = create_response.json()["data"]["createTask"]["id"]

    # Luego actualizar
    update_query = f"""
    mutation {{
        updateTask(id: {task_id}, task: {{
            title: "Updated GraphQL Task",
            completed: true
        }}) {{
            id
            title
            completed
        }}
    }}
    """
    update_response = client.post("/graphql", json={"query": update_query})
    assert update_response.status_code == 200

    updated_task = update_response.json()["data"]["updateTask"]
    assert updated_task["title"] == "Updated GraphQL Task"
    assert updated_task["completed"] == True


def test_delete_task_mutation():
    """Prueba mutación de eliminación de tarea en GraphQL"""
    # Crear tarea para eliminar
    create_query = """
    mutation {
        createTask(task: {title: "Task to Delete"}) {
            id
        }
    }
    """
    create_response = client.post("/graphql", json={"query": create_query})
    task_id = create_response.json()["data"]["createTask"]["id"]

    # Eliminar tarea
    delete_query = f"""
    mutation {{
        deleteTask(id: {task_id})
    }}
    """
    delete_response = client.post("/graphql", json={"query": delete_query})
    assert delete_response.status_code == 200

    deletion_result = delete_response.json()["data"]["deleteTask"]
    assert deletion_result == True
