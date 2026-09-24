#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (top: 1pt + black, bottom: 0.5pt + black) } else if y == 7 { (bottom: 1pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Samples*], [*Mittelwert [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [Camera], `rmw_fastrtps_cpp`, [10], [14732,03], [1473,2028], [245,5338], [0,00\%], [0,00\%],
    [Camera], `rmw_zenoh_cpp`, [10], [3440,72], [344,0716], [57,3453], [0,00\%], [0,00\%],
    [IMU], `rmw_fastrtps_cpp`, [10], [40,36], [4,0363], [0,6727], [0,00\%], [0,00\%],
    [IMU], `rmw_zenoh_cpp`, [10], [35,79], [3,5793], [0,5966], [0,00\%], [0,00\%],
    [LiDAR], `rmw_fastrtps_cpp`, [10], [63,53], [6,3530], [1,0588], [0,00\%], [0,00\%],
    [LiDAR], `rmw_zenoh_cpp`, [10], [27,37], [2,7372], [0,4562], [0,00\%], [0,00\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Versuchswiederholungen (6 Hops)],
)
