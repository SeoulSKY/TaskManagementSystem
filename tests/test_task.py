import pytest

from task import Priority, Task, TaskManager

tasks = [
    Task("Task 1", "Description 1", Priority.LOW),
    Task("Task 2", "Description 2", Priority.MEDIUM),
    Task("Task 3", "Description 3", Priority.HIGH),
    Task("Task 4", "Description 4", Priority.LOW),
    Task("Task 5", "Description 5", Priority.HIGH),
    Task("Task 6", "Description 6", Priority.MEDIUM),
]

def test_add_task() -> None:
    """Test the add_task method."""
    manager = TaskManager()
    task = tasks[0]

    assert len(manager) == 0

    manager.add_task(task)
    assert len(manager) == 1

    with pytest.raises(ValueError, match="exists"):
        manager.add_task(task)


def test_add_tasks() -> None:
    """Test the add_tasks method."""
    manager = TaskManager()

    manager.add_tasks([])
    assert len(manager) == 0

    manager.add_tasks(tasks)
    assert len(manager) == len(tasks)

    with pytest.raises(ValueError, match="exists"):
        manager.add_tasks([tasks[0]])

def test_get_all_tasks() -> None:
    """Test the get_all_tasks method."""
    manager = TaskManager()
    assert len(list(manager.get_all_tasks())) == 0

    manager.add_tasks(tasks)

    all_tasks = list(manager.get_all_tasks())
    assert len(all_tasks) == len(tasks)

    assert sorted(all_tasks, reverse=True) == all_tasks

if __name__ == "__main__":
    pytest.main()
