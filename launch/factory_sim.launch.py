from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="smart_factory_mrs",
                executable="factory_sim",
                name="factory_sim",
                output="screen",
            )
        ]
    )
