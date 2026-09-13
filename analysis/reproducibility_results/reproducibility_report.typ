#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1pt + black) } else if y == 1 { (bottom: 0.5pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Runs*], [*Samples*], [*Mittel [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [Camera], `rmw_fastrtps_cpp`, [3], [2000], [820,080.29], [410.0401], [68.3400], [0.07\%], [0.13\%],
    [Camera], `rmw_cyclonedds_cpp`, [3], [2000], [846,779.47], [423.3897], [70.5650], [0.18\%], [0.35\%],
    [Camera], `rmw_fastrtps_dynamic_cpp`, [3], [2000], [819,260.66], [409.6303], [68.2717], [0.59\%], [1.17\%],
    [Camera], `rmw_zenoh_cpp`, [3], [2000], [1,324,827.10], [662.4135], [110.4023], [0.60\%], [1.11\%],
    [IMU], `rmw_fastrtps_cpp`, [3], [2000], [2,803.47], [1.4017], [0.2336], [0.20\%], [0.39\%],
    [IMU], `rmw_fastrtps_dynamic_cpp`, [3], [2000], [2,794.78], [1.3974], [0.2329], [1.05\%], [2.09\%],
    [IMU], `rmw_zenoh_cpp`, [3], [2000], [4,247.04], [2.1235], [0.3539], [5.66\%], [10.87\%],
    [IMU], `rmw_cyclonedds_cpp`, [3], [2000], [2,355.46], [1.1777], [0.1963], [6.33\%], [12.60\%],
    [Lidar], `rmw_zenoh_cpp`, [3], [2000], [5,268.29], [2.6341], [0.4390], [0.10\%], [0.17\%],
    [Lidar], `rmw_fastrtps_cpp`, [3], [2000], [3,533.53], [1.7668], [0.2945], [0.45\%], [0.87\%],
    [Lidar], `rmw_cyclonedds_cpp`, [3], [2000], [3,212.94], [1.6065], [0.2677], [0.50\%], [0.88\%],
    [Lidar], `rmw_fastrtps_dynamic_cpp`, [3], [2000], [3,518.65], [1.7593], [0.2932], [1.13\%], [2.18\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Testläufe (6 Hops)],
)
