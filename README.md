## Prerrequisitos (equipo destino)

**Probado en la máquina origen:**
- Ubuntu **24.04.3 LTS (noble)**
- ROS 2 **Jazzy** (`ROS_DISTRO=jazzy`, `ROS_VERSION=2`, `ROS_PYTHON_VERSION=3`)
- Python **3.12.3**
- rosdep **0.26.0**
- Gazebo Sim (gz) **8.9.0 (Harmonic)**

### Instalación mínima

```bash
sudo apt update

# ROS 2 Jazzy (incluye rviz2, tf2, etc.)
sudo apt install -y ros-jazzy-desktop python3-colcon-common-extensions python3-rosdep git

# Gazebo Sim 8.x (Harmonic)
sudo apt install -y gz-harmonic

# Puente ROS<->GZ y Octomap usados en este repo
sudo apt install -y ros-jazzy-ros-gz-bridge ros-jazzy-octomap-ros

# Inicializar rosdep (si es primera vez en la máquina)
sudo rosdep init 2>/dev/null || true
rosdep update



cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```
![Gz](./Captura%20desde%202025-10-04%2020-21-01.png)

