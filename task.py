"""Provides classes for task manager."""

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum


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


@dataclass(frozen=True)
class Task:
    """Contains the values of a task."""

    title: str
    description: str
    priority: Priority

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
        """Initialize the task manager with an empty task."""
        self._tasks: list[dict[str, Task]] = [{} for _ in range(len(Priority))]

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

    def remove_task(self, title: str) -> Task:
        """Remove a task by its title.
        Time complexity: ``O(1)``.

        :param title: Title of the task to remove.
        :return: The removed task.
        :raises ValueError: If there is no task with the given title.
        """
        task = self.get_task(title)
        return self._tasks[task.priority].pop(task.title)

    def update_task(self, task: Task) -> None:
        """Update an existing task.
        Time complexity: ``O(1)``.

        :param task: Task to update.
        :raises ValueError: If there is no task with the title in the given task.
        """
        self.remove_task(task.title)
        self._tasks[task.priority][task.title] = task

    def get_task(self, title: str) -> Task:
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


    def get_all_tasks(self) -> Iterable[Task]:
        """Get all tasks sorted by their priority.
        Time complexity: ``O(n)`` where n is the number of tasks.

        :return: All tasks that are sorted by priority from highest to lowest.
        """
        tasks = []
        for priority in reversed(Priority):
            tasks.extend(self._tasks[priority].values())

        return tasks

    def __len__(self) -> int:
        """Get the total number of tasks.
        Time complexity: ``O(1)``.

        :return: Total number of tasks.
        """
        return sum(len(tasks) for tasks in self._tasks)
