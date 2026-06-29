#!/bin/bash

# "rmw_connextdds"
MIDDLEWARES=("rmw_zenoh_cpp" "rmw_fastrtps_cpp" "rmw_cyclonedds_cpp" "rmw_fastrtps_dynamic_cpp")

for rmw in "${MIDDLEWARES[@]}"; do
    source ros_source.bash

    echo "=== Set Middleware $rmw ==="
    export RMW_IMPLEMENTATION=$rmw

    if [ "$rmw" = "rmw_zenoh_cpp" ]; then
        echo "=== Starting Zenoh Router ==="
        ros2 run rmw_zenoh_cpp rmw_zenohd &
        ZENOH_PID=$!
        sleep 2 
    fi

    echo "=== Start Measurement - Imu ==="
    ros2 launch imu_cpp imu_launch.py

    echo "=== Start Measurement - Camera ==="
    ros2 launch camera_cpp camera_launch.py

    echo "=== Start Measurement - Lidar ==="
    ros2 launch lidar_cpp lidar_launch.py
    
    # Stop ROS-Daemon 
    ros2 daemon stop 2>/dev/null

    if [ -n "$ZENOH_PID" ]; then
        echo "=== Stopping Zenoh Router ==="
        kill "$ZENOH_PID"
        wait "$ZENOH_PID" 2>/dev/null
        unset ZENOH_PID
    fi
    
    echo "=== Finished Benchmarking for $rmw ==="
    echo "----------------------------------------"
done