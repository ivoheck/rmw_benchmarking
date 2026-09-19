#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1pt + black) } else if y == 1 { (bottom: 0.5pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Runs*], [*Samples*], [*Mittelwert [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [IMU], `rmw_connextdds`, [1], [250], [360.55], [1.4422], [0.2404], [0.00\%], [0.00\%],
    [IMU], `rmw_cyclonedds_cpp`, [1], [250], [228.93], [0.9157], [0.1526], [0.00\%], [0.00\%],
    [IMU], `rmw_fastrtps_cpp`, [1], [250], [340.73], [1.3629], [0.2272], [0.00\%], [0.00\%],
    [IMU], `rmw_zenoh_cpp`, [1], [250], [427.83], [1.7113], [0.2852], [0.00\%], [0.00\%],
    [Lidar], `rmw_connextdds`, [1], [250], [569.57], [2.2783], [0.3797], [0.00\%], [0.00\%],
    [Lidar], `rmw_cyclonedds_cpp`, [1], [250], [468.85], [1.8754], [0.3126], [0.00\%], [0.00\%],
    [Lidar], `rmw_fastrtps_cpp`, [1], [250], [579.77], [2.3191], [0.3865], [0.00\%], [0.00\%],
    [Lidar], `rmw_zenoh_cpp`, [1], [250], [666.81], [2.6672], [0.4445], [0.00\%], [0.00\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Testläufe (6 Hops)],
)
