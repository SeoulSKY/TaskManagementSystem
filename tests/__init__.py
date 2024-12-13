"""test suites."""

from task import Priority, Task

tasks = [
    Task(title="Task 1", description="Description 1", priority=Priority.LOW),
    Task(title="Task 2", description="Description 2", priority=Priority.MEDIUM),
    Task(title="Task 3", description="Description 3", priority=Priority.HIGH),
    Task(title="Task 4", description="Description 4", priority=Priority.LOW),
    Task(title="Task 5", description="Description 5", priority=Priority.HIGH),
    Task(title="Task 6", description="Description 6", priority=Priority.MEDIUM),
]
