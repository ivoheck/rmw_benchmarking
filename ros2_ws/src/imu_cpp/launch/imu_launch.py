import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    base_launch_dir = os.path.join(
        get_package_share_directory('base_package_cpp'), 'launch', 'base_launch.py'
    )

    declare_run_number = DeclareLaunchArgument(
        'run_number',
        default_value='-1'
    )

    declare_node_count = DeclareLaunchArgument(
        'node_count',
        default_value='-1'
    )

    declare_messurement_count = DeclareLaunchArgument(
        'messurement_count',
        default_value='-1'
    )

    run_number_conf = LaunchConfiguration('run_number')
    node_count_conf = LaunchConfiguration('node_count')
    messurement_count_conf = LaunchConfiguration('messurement_count')

    included_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(base_launch_dir),
        launch_arguments={
            'topic_name': 'imu',
            'package_name': 'imu_cpp',
            'run_number': run_number_conf,
            'node_count': node_count_conf,
            'messurement_count': messurement_count_conf,
        }.items()
    )

    return LaunchDescription([
        declare_run_number,
        declare_node_count,
        declare_messurement_count,
        included_launch
    ])