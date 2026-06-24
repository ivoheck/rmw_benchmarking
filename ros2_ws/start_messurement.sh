#!/bin/bash

source ros_source.bash

# "rmw_zenoh_cpp"
MIDDLEWARES=("rmw_fastrtps_cpp" "rmw_connextdds" "rmw_cyclonedds_cpp" "rmw_fastrtps_dynamic_cpp")

for rmw in "${MIDDLEWARES[@]}"; do
    echo "=== Set Middleware $rmw ==="
    export RMW_IMPLEMENTATION=$rmw

    echo "=== Start Messurement - Imu ==="
    ros2 launch imu imu_launch.py

    # echo "=== Start Messurement - Camera ==="
    # ros2 launch camera camera_launch.py

    echo "=== Start Messurement - Lidar ==="
    ros2 launch lidar lidar_launch.py
    
    # Stop ROS-Daemon 
    ros2 daemon stop 2>/dev/null
done