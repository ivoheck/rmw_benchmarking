from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import Image

class BaseProperties():
    custom_qos = QoSProfile(
            depth=10,  
            reliability=ReliabilityPolicy.BEST_EFFORT, 
            durability=DurabilityPolicy.VOLATILE        
        )
    
    msg_type = Image
    topic_prefix = 'camera'