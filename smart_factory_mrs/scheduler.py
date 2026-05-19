from smart_factory_mrs.factory_map import travel_distance
from smart_factory_mrs.models import Robot, Task, TaskStatus


class Scheduler:
    def __init__(self, robots: list[Robot], tasks: list[Task]):
        self.robots = robots
        self.tasks = tasks
        self.last_reason = "initial assignment"

    def reorder_sequence_for_v3_before_v2(self) -> None:
        sequence = {"V1": 0, "V3": 1, "V2": 2, "X": -1}
        for task in self.tasks:
            task.sequence_index = sequence.get(task.product, task.sequence_index)
        self.last_reason = "production sequence changed: V1 -> V3 -> V2"

    def delay_v2_part(self, current_time: int, delay: int = 8) -> None:
        for task in self.tasks:
            if task.product == "V2" and task.status != TaskStatus.DONE:
                task.ready_time = max(task.ready_time, current_time + delay)
                if task.status == TaskStatus.WAITING:
                    task.status = TaskStatus.DELAYED
        self.last_reason = f"V2 part delayed until t={current_time + delay}"

    def insert_urgent_task(self, task: Task) -> None:
        if not any(existing.task_id == task.task_id for existing in self.tasks):
            self.tasks.append(task)
        self.last_reason = "urgent task inserted"

    def reschedule(self, current_time: int) -> list[str]:
        logs = [f"[Scheduler] Reschedule reason: {self.last_reason}"]
        available_tasks = [
            task
            for task in self.tasks
            if task.status in {TaskStatus.WAITING, TaskStatus.ASSIGNED, TaskStatus.DELAYED}
        ]

        logs.extend(self._preempt_for_urgent_task(current_time))

        for task in available_tasks:
            if task.ready_time <= current_time and task.status == TaskStatus.DELAYED:
                task.status = TaskStatus.WAITING
            if task.status == TaskStatus.ASSIGNED:
                task.status = TaskStatus.WAITING
                task.assigned_robot = None

        idle_robots = [robot for robot in self.robots if robot.is_idle()]
        candidates = [
            task
            for task in available_tasks
            if task.status == TaskStatus.WAITING and task.ready_time <= current_time
        ]
        candidates.sort(key=lambda task: self._task_priority_key(task, current_time))

        for robot in idle_robots:
            if not candidates:
                break
            best_task = min(candidates, key=lambda task: self._assignment_cost(robot, task, current_time))
            self._assign(robot, best_task, current_time)
            candidates.remove(best_task)
            logs.append(
                f"[Scheduler] {best_task.task_id}({best_task.product}) -> {robot.robot_id}, "
                f"cost={self._assignment_cost(robot, best_task, current_time):.2f}"
            )

        if len(logs) == 1:
            logs.append("[Scheduler] No new assignment was needed.")
        return logs

    def _task_priority_key(self, task: Task, current_time: int) -> tuple[int, int, int, int]:
        lateness = max(0, current_time - task.due_time)
        return (-task.priority, task.sequence_index, task.due_time, -lateness)

    def _assignment_cost(self, robot: Robot, task: Task, current_time: int) -> float:
        distance = travel_distance(robot.location, task.pickup, task.dropoff)
        finish_time = current_time + distance
        due_penalty = max(0.0, finish_time - task.due_time) * 3.0
        sequence_penalty = task.sequence_index * 2.0
        urgent_bonus = -20.0 if task.urgent else 0.0
        return distance + due_penalty + sequence_penalty - task.priority + urgent_bonus

    def _assign(self, robot: Robot, task: Task, current_time: int) -> None:
        task.status = TaskStatus.IN_PROGRESS
        task.assigned_robot = robot.robot_id
        robot.current_task = task
        robot.remaining_travel = travel_distance(robot.location, task.pickup, task.dropoff)

    def _preempt_for_urgent_task(self, current_time: int) -> list[str]:
        urgent_waiting = [
            task
            for task in self.tasks
            if task.urgent and task.status == TaskStatus.WAITING and task.ready_time <= current_time
        ]
        if not urgent_waiting or any(robot.is_idle() for robot in self.robots):
            return []

        interruptible = [
            robot
            for robot in self.robots
            if robot.current_task is not None and not robot.current_task.urgent
        ]
        if not interruptible:
            return []

        robot = max(interruptible, key=lambda item: item.remaining_travel)
        interrupted_task = robot.current_task
        interrupted_task.status = TaskStatus.WAITING
        interrupted_task.assigned_robot = None
        robot.current_task = None
        robot.remaining_travel = 0.0
        return [
            f"[Scheduler] {robot.robot_id} interrupted {interrupted_task.task_id} "
            "to handle an urgent task."
        ]
