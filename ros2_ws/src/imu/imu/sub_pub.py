import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from imu.base_properties import BaseProperties

class SubPubPublisher(Node):

    def __init__(self):
        super().__init__('sub_pub_publisher')

        self.declare_parameter('sub_topic', 'error')
        self.declare_parameter('pub_topic', 'error')
        sub_topic_val = self.get_parameter('sub_topic').get_parameter_value().string_value
        pub_topic_val = self.get_parameter('pub_topic').get_parameter_value().string_value


        self.publisher = self.create_publisher(Imu, pub_topic_val, BaseProperties.custom_qos)

        self.subscription = self.create_subscription(
            Imu,
            sub_topic_val,
            self.listener_callback,
            BaseProperties.custom_qos)

    def listener_callback(self, msg):
        self.publisher.publish(msg)



def main(args=None):
    rclpy.init(args=args)

    sub_pub_publisher = SubPubPublisher()
    
    try:
        rclpy.spin(sub_pub_publisher)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        sub_pub_publisher.destroy_node()
        try:
            rclpy.shutdown()
        except Exception:
            pass


if __name__ == '__main__':
    main()