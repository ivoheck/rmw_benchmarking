FROM ros:lyrical-ros-base

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV RTI_NC_LICENSE_ACCEPTED=yes

COPY ros2_ws/ ./ros2_ws/

RUN apt-get update && apt-get install -y --no-install-recommends debconf-utils && \
    echo "rti-connext-dds-7.7.0-common rti-connext-dds-7.7.0-common/accepted-rti-connext-dds-7.7.0-common-license boolean true" | debconf-set-selections && \
    apt-get install -y --no-install-recommends \
    ros-lyrical-rmw-zenoh-cpp \
    ros-lyrical-rmw-fastrtps-cpp \
    ros-lyrical-rmw-cyclonedds-cpp \
    ros-lyrical-rmw-connextdds \
    && rm -rf /var/lib/apt/lists/*

RUN /bin/bash -c "source /opt/ros/lyrical/setup.bash && \
    if [ -f /opt/rti.com/rti_connext_dds-7.7.0/resource/scripts/rtisetenv_x64Linux4gcc8.5.0.bash ]; then \
    source /opt/rti.com/rti_connext_dds-7.7.0/resource/scripts/rtisetenv_x64Linux4gcc8.5.0.bash; \
    fi && \
    cd /app/ros2_ws && \
    colcon build"

RUN chmod +x ./ros2_ws/start_messurement.bash

CMD ["/app/ros2_ws/start_messurement.bash"]