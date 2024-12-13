"""Entry point of the program."""
from pathlib import Path

from fastapi import APIRouter, FastAPI, status
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, RedirectResponse, Response
from starlette.staticfiles import StaticFiles

from task import Priority, Task, TaskManager


class SuccessResponse(JSONResponse):
    """Response for success."""

    def __init__(self, *, status_code: int) -> None:
        """Initialize the success response.
        :param status_code: The status code of the response.
        """
        super().__init__("", status_code=status_code)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public",
          StaticFiles(directory=Path(__file__).parent / "public", html=True))
api_router = APIRouter()
search_router = APIRouter()

manager = TaskManager()


@app.get("/")
def index() -> Response:
    """Redirect all get requests to /public."""
    return RedirectResponse(url="/public")


@api_router.get("/task")
def get_task(title: str) -> Task:
    """Return a task that matches the given title.

    :param title: Title of the task to get.
    :return: A task with the given title.
    """
    try:
        return manager.get_task(title=title)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from None


@api_router.post("/task")
def add_task(task: Task) -> Response:
    """Add a new task.

    :param task: The task to add.
    """
    try:
        manager.add_task(task)
        return SuccessResponse(status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from None


@api_router.put("/task")
def update_task(task: Task) -> Response:
    """Update an existing task.

    :param task: The task to update.
    """
    try:
        manager.update_task(task)
        return SuccessResponse(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from None


@api_router.delete("/task")
def delete_task(title: str) -> Response:
    """Delete a task by its title.

    :param title: Title of the task to delete.
    """
    try:
        manager.delete_task(title)
        return SuccessResponse(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from None


@api_router.get("/tasks")
def get_all_tasks() -> list[Task]:
    """Return all tasks, sorted by their priorities.

    :return: A list of all tasks, sorted by their priorities.
    """
    return list(manager.get_all_tasks())


@api_router.post("/tasks")
def add_tasks(tasks: list[Task]) -> Response:
    """Add new tasks.

    :param tasks: The list of tasks to add.
    """
    try:
        manager.add_tasks(tasks)
        return SuccessResponse(status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from None


@api_router.delete("/tasks")
def clear_tasks() -> Response:
    """Delete all tasks.

    :return: A success response.
    """
    manager.clear_tasks()
    return SuccessResponse(status_code=status.HTTP_204_NO_CONTENT)


@search_router.get("/title")
def search_title(keyword: str) -> list[Task]:
    """Search for tasks that have the given keyword in their title/.

    :param keyword: Keyword to search for.
    :return: Tasks that have the given keyword in their title.
    """
    return list(manager.search_tasks(predicate=lambda t: keyword in t.title))


@search_router.get("/description")
def search_description(keyword: str) -> list[Task]:
    """Search for tasks that have the given keyword in their description.

    :param keyword: Keyword to search for.
    :return: Tasks that have the given keyword in their description.
    """
    return list(manager.search_tasks(predicate=lambda t: keyword in t.description))


@search_router.get("/priority")
def search_priority(priority: Priority) -> list[Task]:
    """Search for tasks with the given priority.

    :param priority: Priority of the tasks to search for.
    :return: Tasks with the given priority.
    """
    return list(manager.get_tasks(priority=priority))


api_router.include_router(search_router, prefix="/search")
app.include_router(api_router, prefix="/api")
