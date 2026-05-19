import sys

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


HELP_TEXT = """
Factory event sender
  1 = change production sequence: V1 -> V3 -> V2
  2 = delay V2 part
  3 = insert urgent task X
  4 = reschedule now
  q = quit
"""


class EventSenderNode(Node):
    def __init__(self):
        super().__init__("factory_event_sender")
        self.publisher = self.create_publisher(String, "factory_sim/event", 10)
        self.get_logger().info(HELP_TEXT)

    def publish_event(self, event_key: str) -> None:
        msg = String()
        msg.data = event_key
        self.publisher.publish(msg)
        self.get_logger().info(f"Published event: {event_key}")


def main(args=None):
    rclpy.init(args=args)
    node = EventSenderNode()
    try:
        while rclpy.ok():
            event_key = input("event> ").strip()
            if event_key == "q":
                break
            if event_key not in {"1", "2", "3", "4"}:
                print("Use 1, 2, 3, 4, or q.", file=sys.stderr)
                continue
            node.publish_event(event_key)
            rclpy.spin_once(node, timeout_sec=0.1)
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
