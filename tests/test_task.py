"""Test cases for task module."""

import pytest

from task import Priority, Task, TaskManager
from tests import tasks


class TestPriority:
    """Test cases for Priority."""

    def test_lt(self) -> None:
        """Test the __lt__ method."""
        assert Priority.LOW < Priority.MEDIUM
        assert Priority.LOW < Priority.HIGH

        with pytest.raises(TypeError):
            _ = Priority.LOW < "hello"

    def test_gt(self) -> None:
        """Test the __gt__ method."""
        assert Priority.HIGH > Priority.MEDIUM
        assert Priority.HIGH > Priority.LOW

        with pytest.raises(TypeError):
            _ = Priority.HIGH > "hello"

    def test_eq(self) -> None:
        """Test the __eq__ method."""
        assert Priority.LOW == Priority.LOW
        assert Priority.LOW != Priority.HIGH

        assert Priority.LOW != "hello"

    def test_missing(self) -> None:
        """Test the _missing_ method."""
        low_values = ["LOW", "Low", "low", 0]
        invalid_values = ["invalid", 0.5]

        for value in low_values:
            assert Priority(value) == Priority.LOW

        for value in invalid_values:
            with pytest.raises(ValueError, match="Priority"):
                Priority(value)


class TestTask:
    """Test cases for Task."""

    def test_hash(self) -> None:
        """Test the __hash__ method."""
        assert hash(tasks[0]) == hash(tasks[0])
        assert hash(tasks[0]) == hash(tasks[0].model_copy())
        assert hash(tasks[0]) != hash(tasks[1])

    def test_eq(self) -> None:
        """Test the __eq__ method."""
        assert tasks[0] == tasks[0]
        assert tasks[0] != tasks[1]
        assert tasks[0] == tasks[0].model_copy()

        assert tasks[0] != "hello"

    def test_lt(self) -> None:
        """Test the __lt__ method."""
        assert tasks[0] < tasks[1]
        assert tasks[1] < tasks[2]

        with pytest.raises(TypeError):
            _ = tasks[0] < "hello"

    def test_index(self) -> None:
        """Test the __index__ method."""
        numbers = [1, 2, 3]
        _ = numbers[Priority.LOW]

class TestTaskManager:
    """Test cases for TaskManager."""

    def test_add_task(self) -> None:
        """Test the add_task method."""
        manager = TaskManager()
        task = tasks[0]

        assert len(manager) == 0

        manager.add_task(task)
        assert len(manager) == 1

        with pytest.raises(ValueError, match="exists"):
            manager.add_task(task)


    def test_add_tasks(self) -> None:
        """Test the add_tasks method."""
        manager = TaskManager()

        manager.add_tasks([])
        assert len(manager) == 0

        manager.add_tasks(tasks)
        assert len(manager) == len(tasks)

        with pytest.raises(ValueError, match="exists"):
            manager.add_tasks([tasks[0]])

    def test_delete_task(self) -> None:
        """Test the delete_task method."""
        manager = TaskManager()
        manager.add_tasks(tasks)

        assert len(manager) == len(tasks)

        manager.delete_task(tasks[0].title)
        assert len(manager) == len(tasks) - 1

        with pytest.raises(ValueError, match="not exist"):
            manager.delete_task(tasks[0].title)

    def test_update_task(self) -> None:
        """Test the update_task method."""
        manager = TaskManager()
        manager.add_tasks(tasks)

        assert len(manager) == len(tasks)

        new_description = "New Description"
        new_priority = Priority.HIGH

        updated_task = tasks[0].model_copy(
            update={"description": new_description, "priority": new_priority}
        )
        manager.update_task(updated_task)

        assert len(manager) == len(tasks)

        for task in manager.get_all_tasks():
            if (task.title == tasks[0].title and task.description == new_description
                    and task.priority == new_priority):
                break
        else:
            pytest.fail(f"Task with title '{tasks[0].title} title, description "
                        f"'{new_description}` and priority '{new_priority}' not found.")

        with pytest.raises(ValueError, match="not exist"):
            manager.update_task(
                Task(title="hello", description="", priority=Priority.LOW)
            )

    def test_get_task(self) -> None:
        """Test the get_task method."""
        manager = TaskManager()
        manager.add_tasks(tasks)

        assert manager.get_task(title=tasks[0].title) == tasks[0]

        with pytest.raises(ValueError, match="not exist"):
            manager.get_task(title="hello")

    def test_get_tasks(self) -> None:
        """Test the get_tasks method."""
        manager = TaskManager()
        manager.add_tasks(tasks)

        for priority in Priority:
            assert (len(list(manager.get_tasks(priority=priority)))
                    == len(list(filter(lambda t: t.priority == priority, tasks))))

    def test_get_all_tasks(self) -> None:
        """Test the get_all_tasks method."""
        manager = TaskManager()
        assert len(list(manager.get_all_tasks())) == 0

        manager.add_tasks(tasks)

        all_tasks = list(manager.get_all_tasks())
        assert len(all_tasks) == len(tasks)

        assert sorted(all_tasks, reverse=True) == all_tasks

    def test_search_tasks(self) -> None:
        """Test the search_tasks method."""
        manager = TaskManager()
        manager.add_tasks(tasks)

        assert len(list(manager.search_tasks(
            predicate=lambda t: t.description == tasks[0].description
        ))) == 1

        assert len(list(manager.search_tasks(
            predicate=lambda t: t.priority == Priority.LOW
        ))) == len(list(filter(lambda t: t.priority == Priority.LOW, tasks)))

    def test_clear_tasks(self) -> None:
        """Test the clear_tasks method."""
        manager = TaskManager()

        manager.clear_tasks()
        assert len(manager) == 0

        manager.add_tasks(tasks)

        assert len(manager) == len(tasks)

        manager.clear_tasks()
        assert len(manager) == 0


if __name__ == "__main__":
    pytest.main(__file__)
