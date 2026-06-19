from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import Shutdown

def generate_launch_description():
    PACKAGE_NAME = 'camera'

    nodes = [
        Node(
            package=PACKAGE_NAME,
            executable='base_pub',
            name='base_pub',
        )
    ]

    for i in range(10):
        sub_topic = PACKAGE_NAME if i == 0 else f'{PACKAGE_NAME}_{i}'
        pub_topic = f'{PACKAGE_NAME}_{i+1}' if i < 4 else f'{PACKAGE_NAME}_final'
        
        nodes.append(
            Node(
                package=PACKAGE_NAME,
                executable='sub_pub',
                name=f'sub_pub_{i+1}', 
                parameters=[{
                    'sub_topic': sub_topic,
                    'pub_topic': pub_topic,
                }]
            )
        )

    nodes.append(
        Node(
            package=PACKAGE_NAME,
            executable='final_sub',
            name='final_sub',
            on_exit=Shutdown()
        )
    )

    return LaunchDescription(nodes)