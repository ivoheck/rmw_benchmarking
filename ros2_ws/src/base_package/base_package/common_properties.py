from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

class CommonProperties:
    custom_qos = QoSProfile(
            depth=10,  
            reliability=ReliabilityPolicy.BEST_EFFORT, 
            durability=DurabilityPolicy.VOLATILE        
        )
    
    node_count = 5
    measurement_count = 1000 #250