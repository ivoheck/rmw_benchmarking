import rclpy
from rclpy.node import Node
from camera.base_properties import BaseProperties
import numpy as np


class BasePublisher(Node):

    def __init__(self):
        super().__init__('base_publisher')

        self.publisher_ = self.create_publisher(BaseProperties.msg_type, BaseProperties.topic_prefix, BaseProperties.custom_qos)
        timer_period = 1 / 1
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.height = 250#2160
        self.width = 500#3840
        num_bytes = self.height * self.width * 3
        random_bytes = np.random.randint(0, 256, size=num_bytes, dtype=np.uint8)
        self.data = random_bytes.tobytes()
        self.get_logger().info('gerate data')

    def timer_callback(self):
        msg = BaseProperties.msg_type()
        msg.header.frame_id = f'camera_frame'
        
        msg.height = self.height
        msg.width = self.width
        msg.encoding = 'rgb8'
        msg.step = msg.width * 3
        msg.data = self.data

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