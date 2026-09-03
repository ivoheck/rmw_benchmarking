#!/bin/bash

SESSION_DATE=$(date +"%Y-%m-%d_%H-%M-%S")
export MEASUREMENT_OUTPUT_DIR="/messurement/$SESSION_DATE"

mkdir -p "$MEASUREMENT_OUTPUT_DIR"
echo "Save Mesurement at: $MEASUREMENT_OUTPUT_DIR"

MIDDLEWARES=("rmw_zenoh_cpp" "rmw_fastrtps_cpp" "rmw_cyclonedds_cpp" "rmw_fastrtps_dynamic_cpp")
SENSORS=("imu" "lidar" "camera")

NUM_RUNS=50
NODE_COUNT=5 # +2 nodes (base pub/final sub)
MESSUREMENT_COUNT=50

START_TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
START_EPOCH=$(date +%s)
METADATA_FILE="$MEASUREMENT_OUTPUT_DIR/metadata.yaml"

cat <<EOF > "$METADATA_FILE"
benchmark_metadata:
  session_name: "$SESSION_DATE"
  start_time: "$START_TIMESTAMP"
  parameters:
    num_runs: $NUM_RUNS
    node_count: $NODE_COUNT
    measurement_count: $MESSUREMENT_COUNT
    sensors: [$(printf '"%s", ' "${SENSORS[@]}" | sed 's/, $//')]
    middlewares: [$(printf '"%s", ' "${MIDDLEWARES[@]}" | sed 's/, $//')]
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
        source ros_source.bash

        echo "=== [Run $RUN_NUM] Set Middleware $rmw ==="
        export RMW_IMPLEMENTATION=$rmw

        # Start Zenoh Router
        if [ "$rmw" = "rmw_zenoh_cpp" ]; then
            echo "=== Starting Zenoh Router ==="
            ros2 run rmw_zenoh_cpp rmw_zenohd &
            ZENOH_PID=$!
            sleep 2 
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

        # Stop Zenoh Router
        if [ -n "$ZENOH_PID" ]; then
            echo "=== Stopping Zenoh Router ==="
            kill "$ZENOH_PID"
            wait "$ZENOH_PID" 2>/dev/null
            unset ZENOH_PID
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