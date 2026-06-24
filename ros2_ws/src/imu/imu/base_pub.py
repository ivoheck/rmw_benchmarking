import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
from base_package.common_properties import CommonProperties

import random
import copy


class BasePublisher(Node):

    def __init__(self):
        super().__init__('base_publisher')

        self.publisher_ = self.create_publisher(Imu, '/imu_data', CommonProperties.custom_qos)
        timer_period = 1 / 30 #500
        self.imu = self.get_imu()
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def get_imu(self):
        msg = Imu()
        msg.header.frame_id = 'imu_link'

        msg.orientation.x = random.uniform(-1.0, 1.0)
        msg.orientation.y = random.uniform(-1.0, 1.0)
        msg.orientation.z = random.uniform(-1.0, 1.0)
        msg.orientation.w = random.uniform(-1.0, 1.0)
        
        # 3. Winkelgeschwindigkeit (Angular Velocity in rad/s)
        msg.angular_velocity.x = random.uniform(-3.14, 3.14)
        msg.angular_velocity.y = random.uniform(-3.14, 3.14)
        msg.angular_velocity.z = random.uniform(-3.14, 3.14)
        
        # 4. Lineare Beschleunigung (Linear Acceleration in m/s²)
        msg.linear_acceleration.x = random.uniform(-9.81, 9.81)
        msg.linear_acceleration.y = random.uniform(-9.81, 9.81)
        msg.linear_acceleration.z = random.uniform(-9.81, 9.81)
        
        # Kovarianzen (Standardmäßig oft -1 im ersten Element, wenn nicht genutzt)
        msg.orientation_covariance[0] = -1.0
        msg.angular_velocity_covariance[0] = -1.0
        msg.linear_acceleration_covariance[0] = -1.0

        return msg

    def timer_callback(self):
        msg = copy.deepcopy(self.imu)
        msg.header.stamp = self.get_clock().now().to_msg()
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