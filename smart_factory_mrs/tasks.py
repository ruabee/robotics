from smart_factory_mrs.models import Task


def create_initial_tasks() -> list[Task]:
    return create_production_batch(batch_number=1, start_time=0)


def create_production_batch(batch_number: int, start_time: int) -> list[Task]:
    prefix = f"B{batch_number}"
    return [
        Task(f"{prefix}_T1", "V1", "A", "W1", "S2", due_time=start_time + 8, sequence_index=0),
        Task(f"{prefix}_T2", "V2", "B", "W2", "S1", due_time=start_time + 13, sequence_index=1),
        Task(f"{prefix}_T3", "V3", "C", "W1", "S3", due_time=start_time + 18, sequence_index=2),
    ]


def create_urgent_task(current_time: int) -> Task:
    return Task(
        f"TX_{current_time}",
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
