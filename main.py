from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class Task(TaskCreate):
    id: int


app = FastAPI(title="Gestion de Tareas API", version="1.0.0")

_tasks: list[Task] = []
_next_id = 1


def reset_state() -> None:
    """Testing helper to reset the in-memory store."""
    global _next_id
    _tasks.clear()
    _next_id = 1


def _get_next_id() -> int:
    global _next_id
    current = _next_id
    _next_id += 1
    return current


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return _tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate) -> Task:
    new_task = Task(id=_get_next_id(), **task.model_dump())
    _tasks.append(new_task)
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> dict[str, str]:
    for index, task in enumerate(_tasks):
        if task.id == task_id:
            _tasks.pop(index)
            return {"detail": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
