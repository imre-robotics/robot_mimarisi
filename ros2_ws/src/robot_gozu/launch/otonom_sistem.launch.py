from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Kamera Düğümü
        Node(
            package='robot_gozu',
            executable='kamera_servisi',
            name='kamera_node'
        ),
        # 2. Beyin Düğümü
        Node(
            package='robot_gozu',
            executable='beyin_servisi',
            name='beyin_node'
        ),
        # 3. Motor Sürücü Düğümü
        Node(
            package='robot_gozu',
            executable='motor_servisi',
            name='motor_node'
        ),
        # 4. Acil Durum (E-Stop) Düğümü
        Node(
            package='guvenlik_sistemi',
            executable='acil_stop_servisi',
            name='acil_stop_node'
        )
    ])