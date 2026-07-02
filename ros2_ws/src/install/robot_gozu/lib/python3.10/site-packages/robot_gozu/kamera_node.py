import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class KameraNode(Node):
    def __init__(self):
        super().__init__('kamera_node')
        self.yayinci = self.create_publisher(String, '/kamera_durumu', 10)
        self.timer = self.create_timer(1.0, self.kare_yakala_ve_yayinla)
        self.get_logger().info("=== [ROS 2] Kamera Düğümü Basariyla Baslatildi ===")

    def kare_yakala_ve_yayinla(self):
        msg = String()
        durum = random.choice(["nesne_bulundu", "nesne_bulundu", "nesne_kayip"])
        msg.data = durum
        self.yayinci.publish(msg)
        self.get_logger().info(f"[YAYIN] /kamera_durumu basligina gonderildi -> {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = KameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Kamera düğümü kapatiliyor...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
