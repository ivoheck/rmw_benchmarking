import rclpy
from camera.base_properties import BaseProperties
from rclpy.node import Node


class SubPub(Node):
    def __init__(self):
        super().__init__('sub_pub')

        self.declare_parameter('sub_topic', 'error')
        self.declare_parameter('pub_topic', 'error')
        sub_topic_val = self.get_parameter('sub_topic').get_parameter_value().string_value
        pub_topic_val = self.get_parameter('pub_topic').get_parameter_value().string_value

        self.publisher = self.create_publisher(BaseProperties.msg_type, pub_topic_val, BaseProperties.custom_qos)

        self.subscription = self.create_subscription(
            BaseProperties.msg_type,
            sub_topic_val,
            self.listener_callback,
            BaseProperties.custom_qos)

    def listener_callback(self, msg):
        self.publisher.publish(msg)



def main(args=None):
    rclpy.init(args=args)

    sub_pub = SubPub()
    try:
        rclpy.spin(sub_pub)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        sub_pub.destroy_node()
        try:
            rclpy.shutdown()
        except Exception:
            pass


if __name__ == '__main__':
    main()