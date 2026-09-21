#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1pt + black) } else if y == 1 { (bottom: 0.5pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Runs*], [*Samples*], [*Mittelwert [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [Camera], `rmw_fastrtps_cpp`, [3], [6250], [2,681,244.85], [428.9992], [71.4999], [0.08\%], [0.15\%],
    [Camera], `rmw_zenoh_cpp`, [3], [6250], [4,123,388.59], [659.7422], [109.9570], [0.24\%], [0.42\%],
    [Camera], `rmw_cyclonedds_cpp`, [3], [6250], [2,611,135.89], [417.7817], [69.6303], [1.73\%], [3.46\%],
    [IMU], `rmw_cyclonedds_cpp`, [3], [6250], [7,782.67], [1.2452], [0.2075], [0.94\%], [1.88\%],
    [IMU], `rmw_zenoh_cpp`, [3], [6250], [13,450.80], [2.1521], [0.3587], [1.51\%], [2.92\%],
    [IMU], `rmw_fastrtps_cpp`, [3], [6250], [10,546.44], [1.6874], [0.2812], [1.96\%], [3.73\%],
    [IMU], `rmw_connextdds`, [3], [6250], [10,242.62], [1.6388], [0.2731], [2.39\%], [4.49\%],
    [Lidar], `rmw_zenoh_cpp`, [3], [6250], [16,619.17], [2.6591], [0.4432], [0.03\%], [0.07\%],
    [Lidar], `rmw_connextdds`, [3], [6250], [12,077.20], [1.9324], [0.3221], [0.34\%], [0.68\%],
    [Lidar], `rmw_cyclonedds_cpp`, [3], [6250], [10,490.13], [1.6784], [0.2797], [0.93\%], [1.81\%],
    [Lidar], `rmw_fastrtps_cpp`, [3], [6250], [12,425.47], [1.9881], [0.3313], [2.33\%], [4.54\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Testläufe (6 Hops)],
)
