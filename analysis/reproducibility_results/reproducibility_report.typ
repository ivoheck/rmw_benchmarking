#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1pt + black) } else if y == 1 { (bottom: 0.5pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Runs*], [*Samples*], [*Mittelwert [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [Camera], `rmw_fastrtps_dynamic_cpp`, [3], [2500], [1,009,255.93], [403.7024], [67.2837], [1.01\%], [2.01\%],
    [Camera], `rmw_zenoh_cpp`, [3], [2500], [1,647,552.25], [659.0209], [109.8368], [1.21\%], [2.15\%],
    [Camera], `rmw_cyclonedds_cpp`, [3], [2500], [1,058,088.56], [423.2354], [70.5392], [3.96\%], [7.69\%],
    [Camera], `rmw_fastrtps_cpp`, [3], [2500], [1,029,126.81], [411.6507], [68.6085], [5.52\%], [11.02\%],
    [IMU], `rmw_fastrtps_cpp`, [3], [2500], [3,794.22], [1.5177], [0.2529], [0.75\%], [1.44\%],
    [IMU], `rmw_fastrtps_dynamic_cpp`, [3], [2500], [3,764.36], [1.5057], [0.2510], [1.21\%], [2.41\%],
    [IMU], `rmw_cyclonedds_cpp`, [3], [2500], [2,961.97], [1.1848], [0.1975], [2.04\%], [4.07\%],
    [IMU], `rmw_zenoh_cpp`, [3], [2500], [5,185.55], [2.0742], [0.3457], [4.27\%], [8.53\%],
    [Lidar], `rmw_fastrtps_cpp`, [3], [2500], [4,481.49], [1.7926], [0.2988], [0.94\%], [1.84\%],
    [Lidar], `rmw_zenoh_cpp`, [3], [2500], [6,691.79], [2.6767], [0.4461], [1.10\%], [2.20\%],
    [Lidar], `rmw_fastrtps_dynamic_cpp`, [3], [2500], [4,490.67], [1.7963], [0.2994], [1.20\%], [2.16\%],
    [Lidar], `rmw_cyclonedds_cpp`, [3], [2500], [4,210.77], [1.6843], [0.2807], [1.74\%], [3.30\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Testläufe (6 Hops)],
)
