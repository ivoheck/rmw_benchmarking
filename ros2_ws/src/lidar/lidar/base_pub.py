import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

import math


class BasePublisher(Node):

    def __init__(self):
        super().__init__('base_publisher')
        custom_qos = QoSProfile(
            depth=10,  
            reliability=ReliabilityPolicy.BEST_EFFORT, 
            durability=DurabilityPolicy.VOLATILE        
        )

        self.publisher_ = self.create_publisher(LaserScan, '/scan', custom_qos)
        timer_period = 1 / 30
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = LaserScan()
        msg.header.frame_id = 'laser_frame'
        
        msg.angle_min = -math.pi / 2      # -90 Grad
        msg.angle_max = math.pi / 2       # +90 Grad
        msg.angle_increment = math.pi / 180
        
        msg.time_increment = 0.0          # Zeit zwischen Messungen [Sekunden]
        msg.scan_time = 0.1               # Zeit für einen kompletten Scan [Sekunden]
        
        msg.range_min = 0.12              # Minimal messbare Distanz
        msg.range_max = 10.0              # Maximal messbare Distanz
        
        num_readings = 181
        
        msg.ranges = [3.5] * num_readings
        
        msg.intensities = [1.0] * num_readings

        msg.header.stamp = self.get_clock().now().to_msg()

        # Nachricht senden
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    base_publisher = BasePublisher()
    
    try:
        rclpy.spin(base_publisher)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        base_publisher.destroy_node()
        try:
            rclpy.shutdown()
        except Exception:
            pass


if __name__ == '__main__':
    main()