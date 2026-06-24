import rclpy
import os

from rclpy.node import Node
from lidar.base_properties import BaseProperties
from rclpy.time import Time
from base_package.common_properties import CommonProperties

RMW_IMPLEMENTATION = os.environ.get('RMW_IMPLEMENTATION', 'error')
file_path = f'/home/ivo/PersonalData/UniKram/Haw_sem_2/Protocol Engineering/code/messurement/lidar_results_{RMW_IMPLEMENTATION}.txt'

class FinalSub(Node):

    def __init__(self):
        super().__init__('final_sub')

        self.subscription = self.create_subscription(
            BaseProperties.msg_type,
            'scan_final',
            self.listener_callback,
            CommonProperties.custom_qos)
        
        self.count = 0
        self.messurement = []

    def listener_callback(self, msg):
        now = self.get_clock().now()
        msg_time = Time.from_msg(msg.header.stamp)
    
        diff = now - msg_time

        if self.count <= CommonProperties.measurement_count:
            self.messurement.append(diff)
            self.get_logger().info('Diff in Seconds: %f' % (diff.nanoseconds / 1e9))

        else:
            self.save_data()
    
        self.count += 1
        self.get_logger().info('Diff in Seconds: %f' % (diff.nanoseconds / 1e9))
        

    def save_data(self):
        with open(file_path, mode='w') as file:
            file.writelines(f"{ts}\n" for ts in self.messurement)

        self.get_logger().info('Saved data')
        self.context.shutdown()

def main(args=None):
    rclpy.init(args=args)

    final_sub = FinalSub()
    
    try:
        rclpy.spin(final_sub)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        final_sub.destroy_node()
        try:
            rclpy.shutdown()
        except Exception:
            pass


if __name__ == '__main__':
    main()