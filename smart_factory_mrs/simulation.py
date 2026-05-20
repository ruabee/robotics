from math import ceil

from smart_factory_mrs.factory_map import FACTORY_MAP, route_points
from smart_factory_mrs.models import Robot, TaskStatus
from smart_factory_mrs.scheduler import Scheduler
from smart_factory_mrs.tasks import create_initial_tasks, create_production_batch, create_urgent_task

ROBOT_SPEED = 2.0


class FactorySimulation:
    def __init__(self):
        self.time = 0
        self.batch_number = 1
        self.robots = [Robot("R1", "W1"), Robot("R2", "W2")]
        self.scheduler = Scheduler(self.robots, create_initial_tasks())

    def step(self) -> list[str]:
        self.time += 1
        logs = [f"\n=== t={self.time} ==="]
        for robot in self.robots:
            if robot.current_task is None:
                logs.append(f"{robot.robot_id}: idle at {robot.location}")
                continue

            robot.remaining_travel = max(0.0, robot.remaining_travel - ROBOT_SPEED)
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
                robot.total_travel = 0.0

        logs.extend(self._ensure_continuous_production())
        logs.extend(self.scheduler.reschedule(self.time))
        logs.extend(self.map_lines())
        logs.extend(self.status_lines())
        return logs

    def apply_event(self, event_key: str) -> list[str]:
        if event_key == "1":
            self.scheduler.reorder_sequence_for_v3_before_v2()
        elif event_key == "2":
            self.scheduler.delay_v2_part(self.time)
        elif event_key == "3":
            self.scheduler.insert_urgent_task(create_urgent_task(self.time))
        elif event_key in {"4", "r", "R"}:
            self.scheduler.last_reason = "manual reschedule"
        elif event_key in {"o", "O"}:
            self.scheduler.set_obstacle_active(True)
        elif event_key in {"c", "C"}:
            self.scheduler.set_obstacle_active(False)
        else:
            return [f"Unknown event: {event_key}"]
        return self.scheduler.reschedule(self.time)

    def status_lines(self) -> list[str]:
        lines = ["[Status] Robots"]
        lines.append(f"  obstacle_active={self.scheduler.obstacle_active}")
        for robot in self.robots:
            task_id = robot.current_task.task_id if robot.current_task else "-"
            route = self._route_text(robot)
            progress = self._progress_bar(robot)
            lines.append(
                f"  {robot.robot_id}: loc={robot.location}, task={task_id}, "
                f"{route}, {progress}, done={robot.completed_tasks}"
            )

        lines.append("[Status] Tasks")
        for task in sorted(self.scheduler.tasks, key=lambda item: (item.sequence_index, item.due_time)):
            lines.append(
                f"  {task.task_id}: product={task.product}, status={task.status.value}, "
                f"ready={task.ready_time}, due={task.due_time}, robot={task.assigned_robot}"
            )
        return lines

    def _ensure_continuous_production(self) -> list[str]:
        active_tasks = [
            task
            for task in self.scheduler.tasks
            if not task.urgent and task.status != TaskStatus.DONE
        ]
        if active_tasks:
            return []

        self.batch_number += 1
        new_tasks = create_production_batch(self.batch_number, self.time)
        self.scheduler.tasks.extend(new_tasks)
        self.scheduler.last_reason = f"new production batch B{self.batch_number} released"
        return [
            f"[Production] Batch B{self.batch_number} released: "
            + ", ".join(task.task_id for task in new_tasks)
        ]

    def map_lines(self) -> list[str]:
        grid = [["." for _ in range(9)] for _ in range(7)]
        for name, location in FACTORY_MAP.items():
            grid[int(location.y)][int(location.x)] = name

        for robot in self.robots:
            x, y = self._robot_grid_position(robot)
            current = grid[y][x]
            grid[y][x] = robot.robot_id if current == "." else f"{current}/{robot.robot_id}"

        lines = ["[Factory Map]"]
        for y in range(6, -1, -1):
            cells = [f"{grid[y][x]:^7}" for x in range(9)]
            lines.append("".join(cells))
        return lines

    def _robot_grid_position(self, robot: Robot) -> tuple[int, int]:
        x, y = self.robot_xy(robot)
        return round(x), round(y)

    def robot_xy(self, robot: Robot) -> tuple[float, float]:
        if robot.current_task is None or robot.total_travel <= 0.0:
            location = FACTORY_MAP[robot.location]
            return location.x, location.y

        task = robot.current_task
        points = route_points(robot.location, task.pickup, task.dropoff, self.scheduler.obstacle_active)
        progress = 1.0 - (robot.remaining_travel / robot.total_travel)
        return self._point_on_path(points, progress)

    def _point_on_path(self, points, progress: float) -> tuple[float, float]:
        if len(points) == 1:
            return points[0].x, points[0].y
        segment_lengths = [
            start.distance_to(end)
            for start, end in zip(points, points[1:])
        ]
        total = sum(segment_lengths)
        if total <= 0.0:
            return points[-1].x, points[-1].y

        target_distance = max(0.0, min(total, total * progress))
        traveled = 0.0
        for start, end, length in zip(points, points[1:], segment_lengths):
            if traveled + length >= target_distance:
                segment_progress = 0.0 if length <= 0.0 else (target_distance - traveled) / length
                x = start.x + (end.x - start.x) * segment_progress
                y = start.y + (end.y - start.y) * segment_progress
                return max(0.0, min(8.0, x)), max(0.0, min(6.0, y))
            traveled += length
        return points[-1].x, points[-1].y

    def _route_text(self, robot: Robot) -> str:
        if robot.current_task is None:
            return "route=-"
        task = robot.current_task
        return f"route={robot.location}->{task.pickup}->{task.dropoff}"

    def _progress_bar(self, robot: Robot) -> str:
        if robot.current_task is None or robot.total_travel <= 0.0:
            return "progress=[----------] 0%"
        progress = 1.0 - (robot.remaining_travel / robot.total_travel)
        filled = max(0, min(10, round(progress * 10)))
        return f"progress=[{'#' * filled}{'-' * (10 - filled)}] {round(progress * 100)}%"
