from collections import deque

import rclpy
from gazebo_msgs.msg import EntityState
from gazebo_msgs.srv import SetEntityState
from rclpy.node import Node
from std_msgs.msg import String

from smart_factory_mrs.simulation import FactorySimulation


class GazeboFactorySimNode(Node):
    def __init__(self):
        super().__init__("gazebo_factory_sim")
        self.simulation = FactorySimulation()
        self.events: deque[str] = deque()
        self.status_pub = self.create_publisher(String, "factory_sim/status", 10)
        self.event_sub = self.create_subscription(String, "factory_sim/event", self.on_event, 10)
        self.set_state_client = self.create_client(SetEntityState, "/set_entity_state")
        self.timer = self.create_timer(1.0, self.on_timer)

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

        lines = self.simulation.step()
        self.publish_robot_states()
        message = "\n".join(lines)
        self.status_pub.publish(String(data=message))
        self.get_logger().info(message)

    def publish_robot_states(self) -> None:
        for robot in self.simulation.robots:
            x, y = self.simulation.robot_xy(robot)
            self.set_entity_pose(robot.robot_id, x, y)

    def set_entity_pose(self, entity_name: str, x: float, y: float) -> None:
        state = EntityState()
        state.name = entity_name
        state.pose.position.x = x
        state.pose.position.y = y
        state.pose.position.z = 0.18
        state.pose.orientation.w = 1.0
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
