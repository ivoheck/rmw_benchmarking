import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy



class SubPubPublisher(Node):

    def __init__(self):
        super().__init__('sub_pub_publisher')

        self.declare_parameter('sub_topic', 'error')
        self.declare_parameter('pub_topic', 'error')
        sub_topic_val = self.get_parameter('sub_topic').get_parameter_value().string_value
        pub_topic_val = self.get_parameter('pub_topic').get_parameter_value().string_value

        custom_qos = QoSProfile(
            depth=10,  
            reliability=ReliabilityPolicy.BEST_EFFORT, 
            durability=DurabilityPolicy.VOLATILE        
        )

        self.publisher = self.create_publisher(LaserScan, pub_topic_val, custom_qos)

        self.subscription = self.create_subscription(
            LaserScan,
            sub_topic_val,
            self.listener_callback,
            custom_qos)

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