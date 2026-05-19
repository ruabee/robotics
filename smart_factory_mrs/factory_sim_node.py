import select
import sys

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from smart_factory_mrs.simulation import FactorySimulation


HELP_TEXT = """
Controls:
  1 = change sequence V1 -> V3 -> V2
  2 = delay V2 part
  3 = insert urgent task X
  r = reschedule now
  q = quit
"""


class FactorySimNode(Node):
    def __init__(self):
        super().__init__("factory_sim")
        self.publisher = self.create_publisher(String, "factory_sim/status", 10)
        self.simulation = FactorySimulation()
        self.timer = self.create_timer(1.0, self.on_timer)
        self.get_logger().info(HELP_TEXT)
        for line in self.simulation.scheduler.reschedule(self.simulation.time):
            self.get_logger().info(line)

    def on_timer(self) -> None:
        event_key = self._read_key_if_available()
        if event_key == "q":
            self.get_logger().info("Shutting down factory simulation.")
            rclpy.shutdown()
            return
        if event_key:
            for line in self.simulation.apply_event(event_key):
                self.get_logger().info(line)

        lines = self.simulation.step()
        message = "\n".join(lines)
        self.publisher.publish(String(data=message))
        self.get_logger().info(message)

    def _read_key_if_available(self) -> str | None:
        if not sys.stdin.isatty():
            return None
        readable, _, _ = select.select([sys.stdin], [], [], 0.0)
        if not readable:
            return None
        return sys.stdin.readline().strip()


def main(args=None):
    rclpy.init(args=args)
    node = FactorySimNode()
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
