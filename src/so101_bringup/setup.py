from setuptools import setup

package_name = 'so101_bringup'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name + '/launch', ['launch/so101_sim.launch.py']),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Fernando',
    maintainer_email='you@example.com',
    description='Launch Gazebo world + ros_gz_bridge + RViz',
    license='BSD',
)