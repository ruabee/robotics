from dataclasses import dataclass, field
from enum import Enum
from math import sqrt


class TaskStatus(str, Enum):
    WAITING = "waiting"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    DELAYED = "delayed"


@dataclass(frozen=True)
class Location:
    name: str
    x: float
    y: float

    def distance_to(self, other: "Location") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass
class Task:
    task_id: str
    product: str
    part: str
    pickup: str
    dropoff: str
    due_time: int
    sequence_index: int
    priority: int = 1
    ready_time: int = 0
    urgent: bool = False
    status: TaskStatus = TaskStatus.WAITING
    assigned_robot: str | None = None

    def is_available(self, current_time: int) -> bool:
        return self.status in {TaskStatus.WAITING, TaskStatus.ASSIGNED} and self.ready_time <= current_time


@dataclass
class Robot:
    robot_id: str
    location: str
    current_task: Task | None = None
    remaining_travel: float = 0.0
    total_travel: float = 0.0
    completed_tasks: list[str] = field(default_factory=list)

    def is_idle(self) -> bool:
        return self.current_task is None
