FROM ros:lyrical-ros-base

WORKDIR /app

COPY ros2_ws/ ./ros2_ws/

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-lyrical-rmw-zenoh-cpp \
    ros-lyrical-rmw-fastrtps-cpp \
    ros-lyrical-rmw-cyclonedds-cpp \
    ros-lyrical-rmw-fastrtps-dynamic-cpp \
    && rm -rf /var/lib/apt/lists/*

RUN /bin/bash -c "source /opt/ros/lyrical/setup.bash && \
    cd /app/ros2_ws && \
    colcon build"

RUN chmod +x ./ros2_ws/start_messurement.bash

CMD ["/bin/bash", "-c", \
    "source /opt/ros/lyrical/setup.bash && \
    source /app/ros2_ws/install/setup.bash && \
    ./ros2_ws/start_messurement.bash"]