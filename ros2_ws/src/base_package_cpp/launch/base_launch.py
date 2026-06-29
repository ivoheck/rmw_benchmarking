from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import Shutdown, OpaqueFunction
from launch.substitutions import LaunchConfiguration

def evaluate_launch(context):
    topic_name = context.perform_substitution(LaunchConfiguration('topic_name'))
    package_name = context.perform_substitution(LaunchConfiguration('package_name'))
    run_number = int(context.perform_substitution(LaunchConfiguration('run_number')))
    node_count = int(context.perform_substitution(LaunchConfiguration('node_count')))
    messurement_count = int(context.perform_substitution(LaunchConfiguration('messurement_count')))

    nodes = [
        Node(
            package=package_name,
            executable='base_publisher',
            name='base_publisher',
        )
    ]

    for i in range(node_count):
        input_topic = topic_name if i == 0 else f'{topic_name}_{i}'
        output_topic = f'{topic_name}_{i+1}' if i < (node_count -1) else f'{topic_name}_final'
        
        nodes.append(
            Node(
                package=package_name,
                executable='subscriber_publisher',
                name=f'subscriber_publisher_{i+1}', 
                parameters=[{
                    'input_topic': input_topic,
                    'output_topic': output_topic,
                }]
            )
        )

    nodes.append(
        Node(
            package=package_name,
            executable='final_subscriber',
            name='final_subscriber',
            parameters=[{
                    'messurement_count': messurement_count,
                    'run_number': run_number,
                }],
            on_exit=Shutdown()
        )
    )

    return nodes

def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=evaluate_launch)
    ])