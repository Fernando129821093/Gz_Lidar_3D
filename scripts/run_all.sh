#!/usr/bin/env bash
set -euo pipefail

# 1) Cargar entorno ROS 2 + workspace
source /opt/ros/jazzy/setup.bash
# Si ya compilaste en esta máquina:
[ -f install/setup.bash ] && source install/setup.bash || true

# 2) Limpiar estado/caché de simulación (opcional)
pkill -f "gz sim" || true
rm -rf ~/.gz/sim/state ~/.gz/sim/worlds ~/.config/gz 2>/dev/null || true

# 3) Lanzar Gazebo con ruta RELATIVA (sin hardcodear /home/fernando)
WORLD_PATH="$(pwd)/models/so101_new_calib/so101_world_local.sdf"
gz sim -r -v 4 "$WORLD_PATH" &
GZ_PID=$!

# 4) Espera breve a que cargue el mundo
sleep 4

# 5) Bridge ROS<->GZ (ajusta el topic si cambia el mundo)
ros2 run ros_gz_bridge parameter_bridge \
  /world/so101_world_local/model/so101/link/gripper_link/sensor/lidar3d/scan/points@sensor_msgs/msg/PointCloud2@gz.msgs.PointCloudPacked \
  --ros-args -r /world/so101_world_local/model/so101/link/gripper_link/sensor/lidar3d/scan/points:=/lidar3d/points &

# 6) TF estático (yaw=1.22173 rad ~ 70°). Ajusta si cambia el frame
ros2 run tf2_ros static_transform_publisher \
  0 0 0 0 1.22173 0 \
  so101/gripper_link/lidar3d \
  so101/gripper_link/lidar3d_corrected &

# 7) Octomap server
ros2 run octomap_server octomap_server_node \
  --ros-args \
  -r /cloud_in:=/lidar3d/points \
  -p frame_id:=so101/gripper_link/lidar3d \
  -p resolution:=0.01 \
  -p max_range:=30.0 &

# 8) RViz (usa ruta local del config)
RVIZ_CFG="$(pwd)/rviz_config.rviz"
if [ -f "$RVIZ_CFG" ]; then
  ros2 run rviz2 rviz2 -d "$RVIZ_CFG" &
else
  ros2 run rviz2 rviz2 &
fi

wait $GZ_PID
