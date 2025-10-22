import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from launch_ros.actions import Node

def generate_launch_description():
    # Rutas: AJUSTA si difieren en tu PC
    sdf_file = os.path.join(
        os.getenv('HOME'),
        'ros2_ws', 'models', 'so101_new_calib', 'so101_world_local.sdf'
    )
    rviz_config = os.path.join(
        os.getenv('HOME'),
        'ros2_ws', 'rviz', 'so101_config.rviz'  # opcional; crea este archivo si quieres
    )
    models_root = os.path.join(os.getenv('HOME'), 'ros2_ws', 'models')

    # Tópico GZ → ROS (tu regla original), con remap a /lidar3d/points
    gz_topic = '/world/so101_world_local/model/so101/link/gripper_link/sensor/lidar3d/scan/points'
    bridge_rule = f'{gz_topic}@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked'

    return LaunchDescription([
        # Para que Gazebo encuentre model://so101_new_calib/...
        SetEnvironmentVariable(name='GZ_SIM_RESOURCE_PATH',
                               value=f"{os.environ.get('GZ_SIM_RESOURCE_PATH', '')}:{models_root}"),

        # Arranca Gazebo Sim en modo headless (-r)
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', sdf_file],
            output='screen'
        ),

        # Bridge de PointCloud2 (un solo proceso puede llevar más reglas si quieres)
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[bridge_rule],
            remappings=[(gz_topic, '/lidar3d/points')],
            output='screen'
        ),

        # RViz (opcional) — comenta este bloque si no quieres abrirlo
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        ),
    ])

