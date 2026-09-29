# ROS 2 RMW Benchmarking

Benchmark that compares the end-to-end latency of four ROS 2 middleware implementations (RMWs)
for three different sensor data types, plus the tooling to run the benchmark in Docker and to
evaluate the resulting data.

**Middlewares under test**

| RMW | Implementation |
| --- | --- |
| `rmw_fastrtps_cpp` | Fast DDS (eProsima) |
| `rmw_cyclonedds_cpp` | Cyclone DDS |
| `rmw_connextdds` | RTI Connext DDS |
| `rmw_zenoh_cpp` | Zenoh |

**Sensors**

| Package | Message type | Rate | QoS |
| --- | --- | --- | --- |
| `imu_cpp` | `sensor_msgs/msg/Imu` | 500 Hz | `SensorDataQoS` |
| `lidar_cpp` | `sensor_msgs/msg/LaserScan` (1081 readings) | 30 Hz | `SensorDataQoS` |
| `camera_cpp` | `sensor_msgs/msg/Image` (1920×1080) | 1 Hz | `keep_last(1).reliable()` |

---

## How the measurement works

Every measurement is a linear chain of ROS 2 nodes. The first node publishes a message with a
`steady_clock` timestamp written into `header.stamp`, every following node simply forwards the
message, and the last node compares its own receive timestamp against the stamp:

```
base_publisher -> subscriber_publisher x5 -> final_subscriber
                     (topic: imu / scan / camera)
```

* The chain consists of one publisher, `NODE_COUNT` (default `5`) forwarding nodes and one
  final subscriber, so a single message crosses **6 hops** (`ros2_ws/src/base_package_cpp/launch/base_launch.py`).
* The final subscriber records `messurement_count` (default `300`) latency values per run, one
  value per line in nanoseconds, then shuts itself down.
* The first 50 values of every file are discarded by the analysis as a warm-up phase.
* Shared memory is disabled for all middlewares

The three sensor packages only differ in the message they publish — the node structure,
launch files and measurement logic are identical.

---

## Running the benchmark locally

Requirements: Docker (with permission to build and run images).

```bash
./run_docker.sh
```

The script:

1. builds the image `ros2-benchmark-image` from the `Dockerfile` (ROS 2 *lyrical* base image plus
   the four RMW packages and a `colcon build` of the workspace),
2. creates `messurement_local/` in the repository root,
3. runs the benchmark container with `messurement_local` mounted at `/messurement`.

A full run takes several hours (the recorded sessions ran ~8 h each). Results are written to:

```
messurement_local/<UTC-timestamp>/
```

Each session directory contains the result files described below plus a `metadata.yaml` with the
benchmark parameters, the resolved software versions of all four RMWs, the kernel version and the
total duration.

> Note: `messurement_local/` is git-ignored. To evaluate a fresh local run, copy or move the
> session folders into `messurement/` (see [Analysis](#analysis)) or point the analysis scripts at
> another input directory.

### Benchmark matrix

`ros2_ws/start_messurement.bash` drives the whole session:

* `NUM_RUNS=30` repetitions per middleware and sensor,
* the order of middlewares, sensors and runs is **rotated on every run** so that systematic
  effects such as warm caches or background load do not always favour the same combination,
* middleware-specific settings are applied per run, e.g. `FASTDDS_BUILTIN_TRANSPORTS=UDPv4`,
  `RMW_CONNEXT_TRANSPORT=UDPv4` and the Zenoh config override that disables shared memory,
* the ROS daemon and all leftover nodes are killed between runs.

Connext DDS is skipped for the camera sensor because that combination did not deliver reliably.

---

## Measurement data

`messurement/` contains the data of the **final** measurement campaign: three independent
sessions, each with 30 runs per sensor and middleware.

```
messurement/2026-09-24_09-27-10Z/
├── metadata.yaml
├── imu_cpp_results_rmw_cyclonedds_cpp_nr_1.txt
├── camera_cpp_results_rmw_connextdds_nr_17.txt
└── ...
```

File naming scheme:

```
<sensor>_cpp_results_<rmw_implementation>_nr_<run_number>.txt
```

Each line contains a single end-to-end latency in nanoseconds:

```
614227077
744372553
96638596
```

---

## Analysis

Requirements: Python 3 with `pandas`, `numpy`, `matplotlib` and `seaborn`.

```bash
cd analysis
./run_analysis.bash
```

All scripts read from `../messurement` (one subdirectory per session) and skip the first 50
values of every file as warm-up.

| Script | Output | Content |
| --- | --- | --- |
| `generate_boxplots.py` | `images/boxplots_all_sensors_combined.pdf` | Latency distribution per sensor and RMW as box plot, outliers above `Q3 + 1.5·IQR` removed, mean and IQR annotated, RMWs sorted by median |
| `generate_results.py` | `images/benchmarks_all_sensors_combined.pdf` | Grouped bar chart with the summed runtime per session, RMW and sensor |
| `calculate_reproducibility.py` | `reproducibility_results/reproducibility_report.typ` | Mean runtime, latency per message along the chain, latency per hop (total ÷ 6), coefficient of variation and relative spread |

---

## Results (final run)

Average latency per hop in milliseconds, and the coefficient of variation (CV) over the three
sessions — lower is better in both columns:

| Sensor | Fast DDS | Cyclone DDS | Connext DDS | Zenoh |
| --- | --- | --- | --- | --- |
| IMU | 0.28 ms (1.05 %) | **0.21 ms (1.10 %)** | 0.27 ms (0.96 %) | 0.38 ms (0.58 %) |
| LiDAR | 0.33 ms (2.00 %) | **0.28 ms (0.66 %)** | 0.32 ms (0.73 %) | 0.44 ms (0.65 %) |
| Camera | **11.82 ms (0.18 %)** | 16.39 ms (0.31 %) | not measured | 16.80 ms (0.57 %) |

Take-aways:

* Cyclone DDS has the lowest latency for the two high-frequency sensors (IMU, LiDAR), while Fast
  DDS wins clearly for the camera — and the difference there is much larger than for the other
  sensors.
* Zenoh is the slowest implementation in all three cases.
* All CV values stay below 2 %, i.e. the measurements are reproducible across the three
  independent sessions.

---

## Kubernetes deployment (optional)

The benchmark can also run unattended on a cluster. Everything for this lives in `deployment/`:

| File | Purpose |
| --- | --- |
| `job.yaml` | Kubernetes `Job` with `completions: 3` (three sessions), 3 CPU / 3 Gi, results written to the mounted PVC |
| `pvc.yaml` | 5 Gi `PersistentVolumeClaim` (`ros-measurement-pvc`) that holds `/messurement` |
| `deploy_job.bash` | Build the image, push it to the GitLab registry, then (re)create the PVC and the job |
| `start_recovery_pod.bash` / `stop_recovery_pod.bash` | Start/stop an Alpine helper pod that mounts the PVC, used to access the data |
| `pull_messurement_data.bash` | Copy the measurement data from the PVC into `deployment/messurement/` |
| `clear_volume_data.bash` | Delete all data on the PVC after a confirmation prompt |

Required environment variables, read from `deployment/.env` (git-ignored):

| Variable | Meaning |
| --- | --- |
| `NAMESPACE` | Kubernetes namespace |
| `IMAGE_TAG` | Tag of the image that is built, pushed and benchmarked |
| `DEPLOY_TOKEN` | Deploy token for the GitLab container registry |

---

## Repository layout

```
.
├── Dockerfile                     ROS 2 lyrical + 4 RMWs + colcon build
├── run_docker.sh                  Build the image and run the benchmark locally
├── analysis/                      Chart and report generation
│   ├── run_analysis.bash          Runs all three scripts
│   ├── generate_boxplots.py
│   ├── generate_results.py
│   ├── calculate_reproducibility.py
│   ├── images/                    Generated charts (git-ignored)
│   └── reproducibility_results/   Generated Typst report
├── deployment/                    Kubernetes Job, PVC and data retrieval scripts
├── messurement/                   Final measurement data (3 sessions)
├── messurement_local/             Output of local runs (git-ignored)
└── ros2_ws/
    ├── start_messurement.bash     Benchmark driver: run matrix, RMW config, metadata
    └── src/
        ├── base_package_cpp/      Shared launch file that builds the node chain
        ├── imu_cpp/               IMU publisher/forwarder/subscriber (500 Hz)
        ├── lidar_cpp/             LiDAR publisher/forwarder/subscriber (30 Hz)
        └── camera_cpp/            Camera publisher/forwarder/subscriber (1 Hz)
```
