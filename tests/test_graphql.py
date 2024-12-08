from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    query = """
    mutation {
        createTask(task: {
            title: "Test Task",
            description: "Test Description"
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
    assert data["data"]["createTask"]["title"] == "Test Task"


def test_list_tasks():
    query = """
    query {
        tasks {
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
    assert isinstance(data["data"]["tasks"], list)


def test_update_task():
    # Primero crear una tarea
    create_query = """
    mutation {
        createTask(task: {title: "Update Task"}) {
            id
        }
    }
    """
    create_response = client.post("/graphql", json={"query": create_query})
    task_id = create_response.json()["data"]["createTask"]["id"]

    # Luego actualizar la tarea
    update_query = f"""
    mutation {{
        updateTask(id: {task_id}, task: {{
            title: "Updated Title",
            completed: true
        }}) {{
            id
            title
            completed
        }}
    }}
    """
    response = client.post("/graphql", json={"query": update_query})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["updateTask"]["title"] == "Updated Title"
    assert data["data"]["updateTask"]["completed"] is True


def test_delete_task():
    # Primero crear una tarea
    create_query = """
    mutation {
        createTask(task: {title: "Delete Task"}) {
            id
        }
    }
    """
    create_response = client.post("/graphql", json={"query": create_query})
    task_id = create_response.json()["data"]["createTask"]["id"]

    # Luego eliminar la tarea
    delete_query = f"""
    mutation {{
        deleteTask(id: {task_id})
    }}
    """
    response = client.post("/graphql", json={"query": delete_query})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["deleteTask"] is True
