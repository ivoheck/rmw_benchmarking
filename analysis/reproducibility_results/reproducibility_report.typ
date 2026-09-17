#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1pt + black) } else if y == 1 { (bottom: 0.5pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Runs*], [*Samples*], [*Mittelwert [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [Camera], `rmw_fastrtps_dynamic_cpp`, [3], [6250], [2,609,108.87], [417.4574], [69.5762], [0.72\%], [1.31\%],
    [Camera], `rmw_zenoh_cpp`, [3], [6250], [4,139,647.45], [662.3436], [110.3906], [1.69\%], [3.19\%],
    [Camera], `rmw_fastrtps_cpp`, [3], [6250], [2,594,954.97], [415.1928], [69.1988], [1.73\%], [3.19\%],
    [IMU], `rmw_fastrtps_cpp`, [3], [6250], [9,307.32], [1.4892], [0.2482], [0.29\%], [0.51\%],
    [IMU], `rmw_fastrtps_dynamic_cpp`, [3], [6250], [9,429.67], [1.5087], [0.2515], [1.70\%], [3.38\%],
    [IMU], `rmw_zenoh_cpp`, [3], [6250], [12,916.53], [2.0666], [0.3444], [2.11\%], [4.06\%],
    [Lidar], `rmw_zenoh_cpp`, [3], [6250], [16,926.82], [2.7083], [0.4514], [0.39\%], [0.70\%],
    [Lidar], `rmw_fastrtps_dynamic_cpp`, [3], [6250], [11,280.58], [1.8049], [0.3008], [0.45\%], [0.81\%],
    [Lidar], `rmw_fastrtps_cpp`, [3], [6250], [11,214.22], [1.7943], [0.2990], [1.06\%], [2.06\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Testläufe (6 Hops)],
)
