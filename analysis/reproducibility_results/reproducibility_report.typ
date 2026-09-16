#figure(
  placement: auto,
  scope: "parent",
  table(
    columns: (auto, auto, auto, auto, 1fr, 1fr, 1fr, 1fr, 1fr),
    stroke: (x, y) => if y == 0 { (bottom: 1pt + black) } else if y == 1 { (bottom: 0.5pt + black) } else { none },
    table.header(
      [*Sensor*], [*RMW*], [*Runs*], [*Samples*], [*Mittelwert [ms]*], [*Kette [ms]*], [*Hop [ms]*], [*CV [%]*], [*Spanne [%]*]
    ),
    [Camera], `rmw_zenoh_cpp`, [3], [5000], [3,333,104.99], [666.6210], [111.1035], [0.23\%], [0.43\%],
    [Camera], `rmw_cyclonedds_cpp`, [3], [5000], [2,075,857.94], [415.1716], [69.1953], [0.35\%], [0.69\%],
    [Camera], `rmw_fastrtps_cpp`, [3], [5000], [2,086,106.02], [417.2212], [69.5369], [0.91\%], [1.82\%],
    [Camera], `rmw_fastrtps_dynamic_cpp`, [3], [5000], [2,047,368.20], [409.4736], [68.2456], [1.75\%], [3.49\%],
    [IMU], `rmw_fastrtps_dynamic_cpp`, [3], [5000], [7,467.00], [1.4934], [0.2489], [0.42\%], [0.83\%],
    [IMU], `rmw_fastrtps_cpp`, [3], [5000], [7,423.60], [1.4847], [0.2475], [1.75\%], [3.49\%],
    [IMU], `rmw_cyclonedds_cpp`, [3], [5000], [5,658.19], [1.1316], [0.1886], [1.86\%], [3.53\%],
    [IMU], `rmw_zenoh_cpp`, [3], [5000], [10,443.26], [2.0887], [0.3481], [1.96\%], [3.88\%],
    [Lidar], `rmw_zenoh_cpp`, [3], [5000], [13,400.40], [2.6801], [0.4467], [0.61\%], [1.13\%],
    [Lidar], `rmw_cyclonedds_cpp`, [3], [5000], [8,460.45], [1.6921], [0.2820], [1.47\%], [2.70\%],
    [Lidar], `rmw_fastrtps_cpp`, [3], [5000], [9,040.22], [1.8080], [0.3013], [1.52\%], [2.83\%],
    [Lidar], `rmw_fastrtps_dynamic_cpp`, [3], [5000], [9,022.71], [1.8045], [0.3008], [1.65\%], [3.30\%],
  ),
  caption: [Reproduzierbarkeits- und Latenzanalyse über 3 Testläufe (6 Hops)],
)
