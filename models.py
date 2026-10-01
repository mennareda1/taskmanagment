from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    task_id: int
    title: str
    priority: str
    description: str
    status: str = "pending"