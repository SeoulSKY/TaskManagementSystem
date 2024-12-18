"""Provides classes for task manager."""

from collections.abc import Callable, Iterable
from enum import Enum
from typing import Self

from pydantic import BaseModel, ConfigDict, field_serializer


class Priority(Enum):
    """Priority of a task."""

    LOW = 0
    MEDIUM = 1
    HIGH = 2

    def __lt__(self, other: object) -> bool:
        """Compare the priority of this task with another object.

        :param other: Object to compare with.
        :return: True if this priority is less than the other priority, False otherwise.
        """
        if not isinstance(other, Priority):
            raise TypeError("The other object must be a Priority.")

        return self.value < other.value

    def __gt__(self, other: object) -> bool:
        """Compare the priority of this task with another object.

        :param other: Object to compare with.
        :return: True if this priority is greater than the other priority,
        False otherwise.
        """
        if not isinstance(other, Priority):
            raise TypeError("The other object must be a Priority.")

        return self.value > other.value

    def __eq__(self, other: object) -> bool:
        """Check if this task is equal to another object.

        :param other: Object to compare with.
        :return: True if this task is equal to another object, False otherwise.
        """
        if not isinstance(other, Priority):
            return False

        return self.value == other.value

    def __index__(self) -> int:
        """Convert the priority as an index.
        :return: Index of the priority.
        """
        return self.value

    @classmethod
    def _missing_(cls, value: object) -> Self:
        """Execute when the value cannot be found in the properties."""
        try:
            if isinstance(value, str):
                return cls[value.upper()]
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid Priority: {value}") from e


class Task(BaseModel):
    """Contains the values of a task."""

    model_config = ConfigDict(frozen=True)

    title: str
    description: str
    priority: Priority

    @field_serializer("priority")
    def serialize_priority(self, priority: Priority, _: type) -> str:
        """Serialize priority field."""
        return priority.name

    def __hash__(self) -> int:
        """Return a hash code for this task.

        :return: Hash code for this task.
        """
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        """Check if this task is equal to another object.

        :return: True if this task is equal to another object, False otherwise.
        """
        if not isinstance(other, Task):
            return False

        return self.title == other.title

    def __lt__(self, other: object) -> bool:
        """Check if this task is less than another task.

        :return: True if this task is less than another task, False otherwise.
        :raise TypeError: If the other object is not a Task
        """
        if not isinstance(other, Task):
            raise TypeError("The other object must be a Task.")

        return self.priority < other.priority


class TaskManager:
    """Provides utilities for managing tasks."""

    def __init__(self) -> None:
        """Initialize the task manager."""
        self._tasks = self._new_task_container()

    @staticmethod
    def _new_task_container() -> list[dict[str, Task]]:
        """Create a new task container.

        :return: New task container.
        """
        return [{} for _ in range(len(Priority))]

    def has_task(self, task: Task) -> bool:
        """Check if the task exists.
        Time complexity: ``O(1)``.

        :param task: Task to check
        :return: True if the task exists, False otherwise
        """
        return task.title in self._tasks[task.priority]

    def add_task(self, task: Task) -> None:
        """Add a task.
        Time complexity: ``O(1)``.

        :param task: Task to add.
        :raises ValueError: If the task with the same title already exists.
        """
        if self.has_task(task):
            raise ValueError(f"Task with the title '{task.title}' already exists.")

        self._tasks[task.priority][task.title] = task

    def add_tasks(self, tasks: Iterable[Task]) -> None:
        """Add multiple tasks.
        Time complexity: ``O(n)`` where n is the number of tasks given.

        :param tasks: Tasks to add.
        :raises ValueError: If the task with the same title already exists.
        """
        for task in tasks:
            self.add_task(task)

    def delete_task(self, title: str) -> Task:
        """Delete a task by its title.
        Time complexity: ``O(1)``.

        :param title: Title of the task to delete.
        :return: The deleted task.
        :raises ValueError: If there is no task with the given title.
        """
        task = self.get_task(title=title)
        return self._tasks[task.priority].pop(task.title)

    def update_task(self, task: Task) -> None:
        """Update an existing task.
        Time complexity: ``O(1)``.

        :param task: Task to update.
        :raises ValueError: If there is no task with the title in the given task.
        """
        self.delete_task(task.title)
        self.add_task(task)

    def get_task(self, *, title: str) -> Task:
        """Get a task by its title.
        Time complexity: ``O(1)``.

        :param title: Title of the task to get.
        :return: The task with the given title.
        :raises ValueError: If there is no task with the given title.
        """
        for priority in Priority:
            task = self._tasks[priority].get(title)
            if task:
                return task

        raise ValueError(f"Task with the title '{title}' does not exist.")

    def get_tasks(self, *, priority: Priority) -> Iterable[Task]:
        """Get tasks that match the given priority
        Time complexity: ``O(1)``.

        :param priority: Priority of the tasks to get
        :return: Tasks with the given priority.
        """
        return self._tasks[priority].values()

    def get_all_tasks(self) -> Iterable[Task]:
        """Lazily get all tasks sorted by their priority.
        Time complexity: ``O(1)`` for calling this function.
        ``O(n)`` for consuming the returned iterable object,
        where n is the number of tasks.

        :return: All tasks that are sorted by priority from highest to lowest.
        """
        for priority in reversed(Priority):
            yield from self.get_tasks(priority=priority)

    def search_tasks(self, *, predicate: Callable[[Task], bool]) -> Iterable[Task]:
        """Lazily search for tasks that satisfy a given predicate.
        Time complexity: ``O(1)`` for calling this function.
        ``O(n)`` for consuming the returned iterable object,
        where n is the number of tasks.

        :param predicate: Predicate function to check for each task.
        :return: Tasks that satisfy the predicate.
        """
        for task in self.get_all_tasks():
            if predicate(task):
                yield task

    def clear_tasks(self) -> None:
        """Clear all tasks.
        Time complexity: ``O(1)``.
        """
        self._tasks = self._new_task_container()

    def __len__(self) -> int:
        """Get the total number of tasks.
        Time complexity: ``O(1)``.

        :return: Total number of tasks.
        """
        return sum(len(tasks) for tasks in self._tasks)
