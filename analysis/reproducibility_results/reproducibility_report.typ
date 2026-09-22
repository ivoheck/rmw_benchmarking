#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (top: 1pt + black, bottom: 0.5pt + black) } else if y == 12 { (bottom: 1pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Samples*], [*Mittelwert [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [Camera], `rmw_cyclonedds_cpp`, [6250], [2611135,89], [417,7817], [69,6303], [1,73\%], [3,46\%],
    [Camera], `rmw_fastrtps_cpp`, [6250], [2681244,85], [428,9992], [71,4999], [0,08\%], [0,15\%],
    [Camera], `rmw_zenoh_cpp`, [6250], [4123388,59], [659,7422], [109,9570], [0,24\%], [0,42\%],
    [IMU], `rmw_cyclonedds_cpp`, [6250], [7782,67], [1,2452], [0,2075], [0,94\%], [1,88\%],
    [IMU], `rmw_fastrtps_cpp`, [6250], [10546,44], [1,6874], [0,2812], [1,96\%], [3,73\%],
    [IMU], `rmw_connextdds`, [6250], [10242,62], [1,6388], [0,2731], [2,39\%], [4,49\%],
    [IMU], `rmw_zenoh_cpp`, [6250], [13450,80], [2,1521], [0,3587], [1,51\%], [2,92\%],
    [Lidar], `rmw_cyclonedds_cpp`, [6250], [10490,13], [1,6784], [0,2797], [0,93\%], [1,81\%],
    [Lidar], `rmw_fastrtps_cpp`, [6250], [12425,47], [1,9881], [0,3313], [2,33\%], [4,54\%],
    [Lidar], `rmw_connextdds`, [6250], [12077,20], [1,9324], [0,3221], [0,34\%], [0,68\%],
    [Lidar], `rmw_zenoh_cpp`, [6250], [16619,17], [2,6591], [0,4432], [0,03\%], [0,07\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Versuchswiederholungen (6 Hops)],
)
