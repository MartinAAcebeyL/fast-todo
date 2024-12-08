# Task List API

This is a RESTful and GraphQL API created with Python, FastAPI, and Strawberry for managing a task list.

## Features

- Complete REST API
- GraphQL Endpoint
- Data validation with Pydantic
- Unit testing with pytest
- Docker support
- Debugger configuration
- Makefile for common commands

## Requirements

- Docker
- make

## Debugger Configuration
The project is configured to use a debugger with the following tools:

- VSCode: Launch configurations included in `.vscode/launch.json`

## Running the Application
### Execution with Docker Compose

```bash
# Build and start the application
docker-compose up --build

# Start the application in the background
docker-compose up -d --build

# Stop the application
docker-compose down
```

## Tests

The project uses `pytest` for unit and integration testing:


```bash
# Run all tests
make test
```

## Endpoints

### API REST

- `GET /tasks/`: List all tasks
- `POST /tasks/`: Create task
- `GET /tasks/{id}`: Get task
- `PUT /tasks/{id}`: Update task
- `DELETE /tasks/{id}`: Delete task

### GraphQL

- Endpoint: `/graphql`
  
