"""Test cases for the main module."""

import pytest
from starlette import status
from starlette.testclient import TestClient

from main import app, manager
from task import Priority
from tests import tasks

client = TestClient(app)
ERROR_KEY = "detail"

@pytest.fixture(autouse=True)
def fixture() -> None:
    """Execute for every test case."""
    yield

    manager.clear_tasks()


def test_index() -> None:
    """Test the endpoint /."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["Content-Type"]


def test_get_task() -> None:
    """Test the endpoint /api/task GET."""
    url = "/api/task"
    task = tasks[0]
    manager.add_task(task)

    response = client.get(url, params={"title": task.title})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == task.model_dump()

    response = client.get(url, params={"title": "hello"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert ERROR_KEY in response.json()

def test_add_task() -> None:
    """Test the endpoint /api/task POST."""
    url = "/api/task"
    task = tasks[0]

    response = client.post(url, json=task.model_dump())
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(url, json=task.model_dump())
    assert response.status_code == status.HTTP_409_CONFLICT
    assert ERROR_KEY in response.json()


def test_update_task() -> None:
    """Test the endpoint /api/task PUT."""
    url = "/api/task"
    task = tasks[0]

    response = client.put(url, json=task.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert ERROR_KEY in response.json()

    manager.add_task(task)

    new_description = "New Description"
    updated_task = task.model_copy(update={"description": new_description})

    response = client.put(url, json=updated_task.model_dump())
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert manager.get_task(title=task.title) == task


def test_delete_task() -> None:
    """Test the endpoint /api/task DELETE."""
    url = "/api/task"
    task = tasks[0]

    response = client.delete(url, params={"title": task.title})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert ERROR_KEY in response.json()

    manager.add_task(task)

    response = client.delete(url, params={"title": task.title})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(manager) == 0


def test_get_all_tasks() -> None:
    """Test the endpoint /api/tasks GET."""
    url = "/api/tasks"

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0

    manager.add_tasks(tasks)

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(tasks)
    for task in response.json():
        assert task in [t.model_dump() for t in tasks]


def test_add_tasks() -> None:
    """Test the endpoint /api/tasks POST."""
    url = "/api/tasks"

    response = client.post(url, json=[task.model_dump() for task in tasks])
    assert response.status_code == status.HTTP_201_CREATED
    assert len(manager) == len(tasks)

    response = client.post(url, json=[task.model_dump() for task in tasks])
    assert response.status_code == status.HTTP_409_CONFLICT
    assert ERROR_KEY in response.json()

    manager.clear_tasks()
    duplicated_tasks = [tasks[0], tasks[0]]

    response = client.post(url, json=[task.model_dump() for task in duplicated_tasks])
    assert response.status_code == status.HTTP_409_CONFLICT
    assert ERROR_KEY in response.json()


def test_clear_tasks() -> None:
    """Test the endpoint /api/tasks DELETE."""
    url = "/api/tasks"

    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    manager.add_tasks(tasks)

    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(manager) == 0


def test_search_title() -> None:
    """Test the endpoint /api/search/title GET."""
    url = "/api/search/title"
    task = tasks[0]
    keyword = task.title[2:5]

    manager.add_task(task)

    response = client.get(url, params={"keyword": keyword})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0] == tasks[0].model_dump()

    response = client.get(url, params={"keyword": "hello"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_search_description() -> None:
    """Test the endpoint /api/search/description GET."""
    url = "/api/search/description"
    task = tasks[0]
    keyword = task.description[3:]

    manager.add_task(task)

    response = client.get(url, params={"keyword": keyword})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0] == tasks[0].model_dump()

    response = client.get(url, params={"keyword": "hello"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


def test_search_priority() -> None:
    """Test the endpoint /api/search/priority GET."""
    url = "/api/search/priority"
    priority = Priority.LOW
    target_tasks = [task for task in tasks if task.priority == priority]

    response = client.get(url, params={"priority": priority.name})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0

    manager.add_tasks(tasks)

    response = client.get(url, params={"priority": priority.name})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(target_tasks)
    assert response.json() == [task.model_dump() for task in target_tasks]


if __name__ == "__main__":
    pytest.main(__file__)
