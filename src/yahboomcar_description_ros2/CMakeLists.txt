cmake_minimum_required(VERSION 3.5)
project(yahboomcar_description_ros2)

find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)

# Instalar recursos (no hay build)
install(DIRECTORY urdf meshes launch
  DESTINATION share/${PROJECT_NAME})

ament_package()
