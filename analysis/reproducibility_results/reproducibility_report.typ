#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1pt + black) } else if y == 1 { (bottom: 0.5pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Runs*], [*Samples*], [*Mittelwert [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [Camera], `rmw_zenoh_cpp`, [3], [6250], [4,142,063.14], [662.7301], [110.4550], [0.37\%], [0.72\%],
    [Camera], `rmw_fastrtps_cpp`, [3], [6250], [2,615,539.61], [418.4863], [69.7477], [0.70\%], [1.39\%],
    [Camera], `rmw_fastrtps_dynamic_cpp`, [3], [6250], [2,554,986.84], [408.7979], [68.1330], [1.47\%], [2.92\%],
    [IMU], `rmw_fastrtps_cpp`, [3], [6250], [9,728.55], [1.5566], [0.2594], [0.71\%], [1.40\%],
    [IMU], `rmw_fastrtps_dynamic_cpp`, [3], [6250], [9,606.32], [1.5370], [0.2562], [1.01\%], [1.90\%],
    [IMU], `rmw_zenoh_cpp`, [3], [6250], [13,488.45], [2.1582], [0.3597], [1.80\%], [3.60\%],
    [Lidar], `rmw_fastrtps_cpp`, [3], [6250], [11,197.48], [1.7916], [0.2986], [0.44\%], [0.84\%],
    [Lidar], `rmw_zenoh_cpp`, [3], [6250], [16,900.31], [2.7040], [0.4507], [1.40\%], [2.46\%],
    [Lidar], `rmw_fastrtps_dynamic_cpp`, [3], [6250], [11,279.87], [1.8048], [0.3008], [2.21\%], [4.38\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Testläufe (6 Hops)],
)
