from smart_factory_mrs.models import Task


def create_initial_tasks() -> list[Task]:
    return [
        Task("T1", "V1", "A", "W1", "S1", due_time=8, sequence_index=0),
        Task("T2", "V2", "B", "W2", "S2", due_time=13, sequence_index=1),
        Task("T3", "V3", "C", "W1", "S3", due_time=18, sequence_index=2),
    ]


def create_urgent_task(current_time: int) -> Task:
    return Task(
        "TX",
        "X",
        "Emergency",
        "W2",
        "S1",
        due_time=current_time + 6,
        sequence_index=-1,
        priority=8,
        ready_time=current_time,
        urgent=True,
    )
