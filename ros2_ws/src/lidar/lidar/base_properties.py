from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import LaserScan

class BaseProperties():
    custom_qos = QoSProfile(
            depth=10,  
            reliability=ReliabilityPolicy.BEST_EFFORT, 
            durability=DurabilityPolicy.VOLATILE        
        )
    
    msg_type = LaserScan