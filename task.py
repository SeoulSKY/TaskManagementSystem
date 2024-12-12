"""Provides classes for task manager."""

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum


class Priority(Enum):
    """Priority of a task."""

    LOW = 0
    MEDIUM = 1
    HIGH = 2


@dataclass
class Task:
    """Contains the values of a task."""

    title: str
    description: str
    priority: Priority

    def __hash__(self) -> int:
        """Return a hash code for this task."""
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        """Check if this task is equal to another object."""
        if not isinstance(other, Task):
            return False

        return self.title == other.title


class TaskManager:
    """Provides utilities for managing tasks."""

    def __init__(self) -> None:
        """Initialize the task manager with an empty task."""
        self._tasks: list[set[Task]] = [set() for _ in range(len(Priority))]

    def add_task(self, task: Task) -> None:
        """Add a task. Time complexity: O(1)."""
        self._tasks[task.priority.value].add(task)

    def add_tasks(self, tasks: Iterable[Task]) -> None:
        """Add multiple tasks. Time complexity: O(n) where n is the number of tasks."""
        for task in tasks:
            self.add_task(task)

    def get_all_tasks(self) -> Iterable[Task]:
        """Get all tasks sorted by their priority.
        Time complexity: O(n) where n is the number of tasks.
        """
        tasks = []
        for priority in Priority:
            tasks.extend(self._tasks[priority.value])

        return tasks.copy()
