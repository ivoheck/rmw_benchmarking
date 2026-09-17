#!/bin/bash

SESSION_DATE=$(date -u +"%Y-%m-%d_%H-%M-%SZ")
export MEASUREMENT_OUTPUT_DIR="/messurement/$SESSION_DATE"

mkdir -p "$MEASUREMENT_OUTPUT_DIR"
echo "Save Mesurement at: $MEASUREMENT_OUTPUT_DIR"

MIDDLEWARES=("rmw_zenoh_cpp" "rmw_fastrtps_cpp" "rmw_cyclonedds_cpp" "rmw_fastrtps_dynamic_cpp")
SENSORS=("imu" "lidar" "camera")

NUM_RUNS=25
NODE_COUNT=5 # +2 nodes (base pub/final sub)
MESSUREMENT_COUNT=300

START_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_EPOCH=$(date +%s)
METADATA_FILE="$MEASUREMENT_OUTPUT_DIR/metadata.yaml"

CONTAINER_IMAGE_TAG="${IMAGE_TAG:-unknown}"

get_pkg_version() {
    local pkg_name="$1"
    local version
    version=$(dpkg-query -W -f='${Version}' "$pkg_name" 2>/dev/null)
    echo "${version:-unknown}"
}

ROS_DISTRO_VER="${ROS_DISTRO:-unknown}"
FAST_DDS_VER=$(get_pkg_version "ros-${ROS_DISTRO:-lyrical}-rmw-fastrtps-cpp")
CYCLONE_DDS_VER=$(get_pkg_version "ros-${ROS_DISTRO:-lyrical}-rmw-cyclonedds-cpp")
ZENOH_RMW_VER=$(get_pkg_version "ros-${ROS_DISTRO:-lyrical}-rmw-zenoh-cpp")

cat <<EOF > "$METADATA_FILE"
benchmark_metadata:
  session_name: "$SESSION_DATE"
  start_time: "$START_TIMESTAMP"
  image_tag: "$CONTAINER_IMAGE_TAG"
  parameters:
    num_runs: $NUM_RUNS
    node_count: $NODE_COUNT
    measurement_count: $MESSUREMENT_COUNT
    shared_memory: true
    sensors: [$(printf '"%s", ' "${SENSORS[@]}" | sed 's/, $//')]
    middlewares: [$(printf '"%s", ' "${MIDDLEWARES[@]}" | sed 's/, $//')]
  software_versions:
    ros_distro: "$ROS_DISTRO_VER"
    rmw_fastrtps_cpp: "$FAST_DDS_VER"
    rmw_cyclonedds_cpp: "$CYCLONE_DDS_VER"
    rmw_zenoh_cpp: "$ZENOH_RMW_VER"
  system_info:
    hostname: "$(hostname)"
    kernel: "$(uname -r)"
EOF

for ((run=0; run<NUM_RUNS; run++)); do
    RUN_NUM=$((run+1))

    echo "========================================"
    echo "   START RUN $RUN_NUM / $NUM_RUNS"
    echo "========================================"

    ROTATED_MIDDLEWARES=()
    for ((i=0; i<${#MIDDLEWARES[@]}; i++)); do
        idx=$(( (i + run) % ${#MIDDLEWARES[@]} ))
        ROTATED_MIDDLEWARES+=("${MIDDLEWARES[$idx]}")
    done

    ROTATED_SENSORS=()
    for ((i=0; i<${#SENSORS[@]}; i++)); do
        idx=$(( (i + run) % ${#SENSORS[@]} ))
        ROTATED_SENSORS+=("${SENSORS[$idx]}")
    done

    for rmw in "${ROTATED_MIDDLEWARES[@]}"; do
        source /opt/ros/lyrical/setup.bash
        source install/setup.bash

        echo "=== [Run $RUN_NUM] Set Middleware $rmw ==="
        export RMW_IMPLEMENTATION=$rmw

        export CYCLONEDDS_URI='<CycloneDDS><Domain><SharedMemory><EnableService>true</EnableService></SharedMemory></Domain></CycloneDDS>'
        export ZENOH_CONFIG_OVERRIDE="transport/shared_memory/enabled=true"
        export FASTDDS_BUILTIN_TRANSPORTS=DEFAULT

        # Start Router 
        ROUTER_PID=""
        if [ "$rmw" = "rmw_zenoh_cpp" ]; then
            echo "=== Starting Zenoh Router ==="
            ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST ros2 run rmw_zenoh_cpp rmw_zenohd --cfg "transport/shared_memory/enabled=true" &
            ROUTER_PID=$!
            sleep 3 
        elif [ "$rmw" = "rmw_cyclonedds_cpp" ]; then
            echo "=== Starting Iceoryx RouDi Daemon for CycloneDDS ==="
            iox-roudi &
            ROUTER_PID=$!
            sleep 3
        fi

        sensor_seq=1
        for sensor in "${ROTATED_SENSORS[@]}"; do
            
            LAUNCH_ARGS="run_number:=$RUN_NUM node_count:=$NODE_COUNT messurement_count:=$MESSUREMENT_COUNT"

            if [ "$sensor" = "imu" ]; then
                echo "=== Start Measurement - Imu (Pos $sensor_seq) ==="
                ros2 launch imu_cpp imu_launch.py $LAUNCH_ARGS
            elif [ "$sensor" = "lidar" ]; then
                echo "=== Start Measurement - Lidar (Pos $sensor_seq) ==="
                ros2 launch lidar_cpp lidar_launch.py $LAUNCH_ARGS
            elif [ "$sensor" = "camera" ]; then
                echo "=== Start Measurement - Camera (Pos $sensor_seq) ==="
                ros2 launch camera_cpp camera_launch.py $LAUNCH_ARGS
            fi

            ((sensor_seq++))
        done

        echo "=== Processes after launch ==="
        ps -eo pid,ppid,rss,cmd --sort=-rss | head -20
        
        # Stop ROS-Daemon
        ros2 daemon stop 2>/dev/null

        # Stop Router
        if [ -n "$ROUTER_PID" ]; then
            echo "=== Stopping Router / Daemon (PID: $ROUTER_PID) ==="
            kill -15 "$ROUTER_PID" 2>/dev/null
            wait "$ROUTER_PID" 2>/dev/null
            sleep 2
            ROUTER_PID=""
        fi
        
        echo "=== Finished Benchmarking for $rmw ==="
        echo "----------------------------------------"
    done
done

END_TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
END_EPOCH=$(date +%s)
DURATION_SECONDS=$((END_EPOCH - START_EPOCH))

cat <<EOF >> "$METADATA_FILE"
  end_time: "$END_TIMESTAMP"
  total_duration_seconds: $DURATION_SECONDS
  status: "COMPLETED"
EOF