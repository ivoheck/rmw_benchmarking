import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    base_launch_dir = os.path.join(
        get_package_share_directory('base_package_cpp'), 'launch', 'base_launch.py'
    )

    declare_run_number = DeclareLaunchArgument(
        'run_number',
        default_value=None
    )

    run_number_conf = LaunchConfiguration('run_number')

    included_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(base_launch_dir),
        launch_arguments={
            'topic_name': 'imu',
            'package_name': 'imu_cpp',
            'run_number': run_number_conf
        }.items()
    )

    return LaunchDescription([included_launch,declare_run_number])
