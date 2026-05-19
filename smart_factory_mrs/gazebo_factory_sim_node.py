from collections import deque
from math import atan2, cos, sin

import rclpy
from gazebo_msgs.msg import EntityState
from gazebo_msgs.srv import SetEntityState
from rclpy.node import Node
from std_msgs.msg import String

from smart_factory_mrs.simulation import FactorySimulation

TIMER_PERIOD = 0.1
SIMULATION_STEP_INTERVAL = 1.0


class GazeboFactorySimNode(Node):
    def __init__(self):
        super().__init__("gazebo_factory_sim")
        self.simulation = FactorySimulation()
        self.events: deque[str] = deque()
        self.step_elapsed = 0.0
        self.motion_elapsed = 0.0
        self.visual_positions = self._simulation_positions()
        self.motion_start_positions = dict(self.visual_positions)
        self.motion_target_positions = dict(self.visual_positions)
        self.status_pub = self.create_publisher(String, "factory_sim/status", 10)
        self.event_sub = self.create_subscription(String, "factory_sim/event", self.on_event, 10)
        self.set_state_client = self.create_client(SetEntityState, "/set_entity_state")
        self.timer = self.create_timer(TIMER_PERIOD, self.on_timer)

        self.get_logger().info("Waiting for Gazebo /set_entity_state service...")
        if not self.set_state_client.wait_for_service(timeout_sec=10.0):
            self.get_logger().warning(
                "Gazebo service /set_entity_state is not available yet. "
                "Robot models may not move until Gazebo finishes loading."
            )
        for line in self.simulation.scheduler.reschedule(self.simulation.time):
            self.get_logger().info(line)
        self.publish_robot_states()
        self.get_logger().info(
            "Gazebo factory simulation started. Publish events with: "
            "ros2 topic pub --once /factory_sim/event std_msgs/msg/String \"{data: '3'}\""
        )

    def on_event(self, msg: String) -> None:
        event_key = msg.data.strip()
        if event_key:
            self.events.append(event_key)

    def on_timer(self) -> None:
        while self.events:
            for line in self.simulation.apply_event(self.events.popleft()):
                self.get_logger().info(line)
            self._start_new_visual_segment()

        self.step_elapsed += TIMER_PERIOD
        self.motion_elapsed += TIMER_PERIOD
        if self.step_elapsed >= SIMULATION_STEP_INTERVAL:
            self.step_elapsed = 0.0
            lines = self.simulation.step()
            self._start_new_visual_segment()
            message = "\n".join(lines)
            self.status_pub.publish(String(data=message))
            self.get_logger().info(message)

        self.publish_robot_states()

    def publish_robot_states(self) -> None:
        self.visual_positions = self._interpolated_positions()
        for robot_id, (x, y) in self.visual_positions.items():
            robot = next(robot for robot in self.simulation.robots if robot.robot_id == robot_id)
            yaw = self._robot_yaw(robot_id)
            if robot.current_task is None:
                yaw = 0.0
            self.set_entity_pose(robot_id, x, y, yaw)

    def set_entity_pose(self, entity_name: str, x: float, y: float, yaw: float) -> None:
        state = EntityState()
        state.name = entity_name
        state.pose.position.x = x
        state.pose.position.y = y
        state.pose.position.z = 0.18
        state.pose.orientation.z = sin(yaw / 2.0)
        state.pose.orientation.w = cos(yaw / 2.0)
        state.reference_frame = "world"

        request = SetEntityState.Request()
        request.state = state
        future = self.set_state_client.call_async(request)
        future.add_done_callback(
            lambda done: self._log_service_error(entity_name, done.exception())
        )

    def _log_service_error(self, entity_name: str, error: Exception | None) -> None:
        if error is not None:
            self.get_logger().warning(f"Failed to move {entity_name}: {error}")

    def _start_new_visual_segment(self) -> None:
        self.visual_positions = self._interpolated_positions()
        self.motion_start_positions = dict(self.visual_positions)
        self.motion_target_positions = self._simulation_positions()
        self.motion_elapsed = 0.0

    def _simulation_positions(self) -> dict[str, tuple[float, float]]:
        return {
            robot.robot_id: self.simulation.robot_xy(robot)
            for robot in self.simulation.robots
        }

    def _interpolated_positions(self) -> dict[str, tuple[float, float]]:
        progress = min(1.0, self.motion_elapsed / SIMULATION_STEP_INTERVAL)
        smooth_progress = progress * progress * (3.0 - 2.0 * progress)
        positions = {}
        for robot_id, start in self.motion_start_positions.items():
            target = self.motion_target_positions[robot_id]
            x = start[0] + (target[0] - start[0]) * smooth_progress
            y = start[1] + (target[1] - start[1]) * smooth_progress
            positions[robot_id] = (x, y)
        return positions

    def _robot_yaw(self, robot_id: str) -> float:
        start = self.motion_start_positions[robot_id]
        target = self.motion_target_positions[robot_id]
        dx = target[0] - start[0]
        dy = target[1] - start[1]
        if abs(dx) < 0.001 and abs(dy) < 0.001:
            return 0.0
        return atan2(dy, dx)


def main(args=None):
    rclpy.init(args=args)
    node = GazeboFactorySimNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == "__main__":
    main()
