from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_share = get_package_share_directory('yahboomcar_description_ros2')
    xacro_file = os.path.join(pkg_share, 'urdf', 'x3plus.urdf.xacro')  # ajusta nombre si difiere
    urdf_out  = os.path.join('/tmp', 'x3plus.urdf')

    # generar URDF
    os.system(f'ros2 run xacro xacro {xacro_file} -o {urdf_out}')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        )
    )
    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-file', urdf_out, '-entity', 'rosmaster_x3plus'],
        output='screen'
    )
    return LaunchDescription([gazebo, spawn])
