#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1pt + black) } else if y == 1 { (bottom: 0.5pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Runs*], [*Samples*], [*Mittelwert [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [IMU], `rmw_cyclonedds_cpp`, [3], [250], [355.40], [1.4216], [0.2369], [3.43\%], [6.57\%],
    [IMU], `rmw_fastrtps_cpp`, [3], [250], [421.48], [1.6859], [0.2810], [3.97\%], [7.94\%],
    [IMU], `rmw_zenoh_cpp`, [3], [250], [516.88], [2.0675], [0.3446], [5.50\%], [9.67\%],
    [IMU], `rmw_connextdds`, [3], [250], [459.54], [1.8381], [0.3064], [6.49\%], [12.98\%],
    [Lidar], `rmw_fastrtps_cpp`, [3], [250], [511.37], [2.0455], [0.3409], [1.36\%], [2.67\%],
    [Lidar], `rmw_cyclonedds_cpp`, [3], [250], [430.48], [1.7219], [0.2870], [1.42\%], [2.63\%],
    [Lidar], `rmw_connextdds`, [3], [250], [528.79], [2.1152], [0.3525], [3.62\%], [6.69\%],
    [Lidar], `rmw_zenoh_cpp`, [3], [250], [647.82], [2.5913], [0.4319], [4.13\%], [7.52\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Testläufe (6 Hops)],
)
