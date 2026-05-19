from math import ceil

from smart_factory_mrs.models import Robot, TaskStatus
from smart_factory_mrs.scheduler import Scheduler
from smart_factory_mrs.tasks import create_initial_tasks, create_urgent_task


class FactorySimulation:
    def __init__(self):
        self.time = 0
        self.robots = [Robot("R1", "W1"), Robot("R2", "W2")]
        self.scheduler = Scheduler(self.robots, create_initial_tasks())

    def step(self) -> list[str]:
        self.time += 1
        logs = [f"\n=== t={self.time} ==="]
        for robot in self.robots:
            if robot.current_task is None:
                logs.append(f"{robot.robot_id}: idle at {robot.location}")
                continue

            robot.remaining_travel = max(0.0, robot.remaining_travel - 1.0)
            task = robot.current_task
            logs.append(
                f"{robot.robot_id}: moving {task.pickup}->{task.dropoff} for "
                f"{task.task_id}({task.product}), remaining={ceil(robot.remaining_travel)}"
            )
            if robot.remaining_travel <= 0.0:
                task.status = TaskStatus.DONE
                robot.location = task.dropoff
                robot.completed_tasks.append(task.task_id)
                logs.append(f"{robot.robot_id}: completed {task.task_id} at {task.dropoff}")
                robot.current_task = None

        logs.extend(self.scheduler.reschedule(self.time))
        logs.extend(self.status_lines())
        return logs

    def apply_event(self, event_key: str) -> list[str]:
        if event_key == "1":
            self.scheduler.reorder_sequence_for_v3_before_v2()
        elif event_key == "2":
            self.scheduler.delay_v2_part(self.time)
        elif event_key == "3":
            self.scheduler.insert_urgent_task(create_urgent_task(self.time))
        elif event_key == "4":
            self.scheduler.last_reason = "manual reschedule"
        else:
            return [f"Unknown event: {event_key}"]
        return self.scheduler.reschedule(self.time)

    def status_lines(self) -> list[str]:
        lines = ["[Status] Robots"]
        for robot in self.robots:
            task_id = robot.current_task.task_id if robot.current_task else "-"
            lines.append(
                f"  {robot.robot_id}: loc={robot.location}, task={task_id}, "
                f"done={robot.completed_tasks}"
            )

        lines.append("[Status] Tasks")
        for task in sorted(self.scheduler.tasks, key=lambda item: (item.sequence_index, item.due_time)):
            lines.append(
                f"  {task.task_id}: product={task.product}, status={task.status.value}, "
                f"ready={task.ready_time}, due={task.due_time}, robot={task.assigned_robot}"
            )
        return lines
