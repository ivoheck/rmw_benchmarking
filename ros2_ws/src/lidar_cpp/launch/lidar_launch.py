import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    base_launch_dir = os.path.join(
        get_package_share_directory('base_package_cpp'), 'launch', 'base_launch.py'
    )

    included_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(base_launch_dir),
        launch_arguments={
            'topic_name': 'scan',
            'package_name': 'lidar_cpp'
        }.items()
    )

    return LaunchDescription([included_launch])
