import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_share = get_package_share_directory("smart_factory_mrs")
    world_path = os.path.join(package_share, "worlds", "smart_factory.world")
    gazebo_launch = os.path.join(
        get_package_share_directory("gazebo_ros"),
        "launch",
        "gazebo.launch.py",
    )

    return LaunchDescription(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(gazebo_launch),
                launch_arguments={"world": world_path}.items(),
            ),
            Node(
                package="smart_factory_mrs",
                executable="gazebo_factory_sim",
                name="gazebo_factory_sim",
                output="screen",
            ),
        ]
    )
