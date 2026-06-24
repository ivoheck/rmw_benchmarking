from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import Shutdown, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from base_package.common_properties import CommonProperties

def evaluate_launch(context):
    topic_name = context.perform_substitution(LaunchConfiguration('topic_name'))
    package_name = context.perform_substitution(LaunchConfiguration('package_name'))

    nodes = [
        Node(
            package=package_name,
            executable='base_pub',
            name='base_pub',
        )
    ]

    for i in range(CommonProperties.node_count):
        sub_topic = topic_name if i == 0 else f'{topic_name}_{i}'
        pub_topic = f'{topic_name}_{i+1}' if i < (CommonProperties.node_count -1) else f'{topic_name}_final'
        
        nodes.append(
            Node(
                package=package_name,
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
            package=package_name,
            executable='final_sub',
            name='final_sub',
            on_exit=Shutdown()
        )
    )

    return nodes

def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=evaluate_launch)
    ])