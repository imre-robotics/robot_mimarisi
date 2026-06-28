import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MotorNode(Node):
    def __init__(self):
        super().__init__('motor_node')
        # /motor_komutlari başlığını dinlemeye başlıyoruz
        self.abonelik = self.create_subscription(
            String, '/motor_komutlari', self.motor_callback, 10)
        self.get_logger().info("=== [ROS 2] Motor Donanim Sürücü Düğümü Aktif ===")

    def motor_callback(self, msg):
        # Gerçek bir sistemde burası mikrodenetleyiciye (seri porttan) veri basar
        komut = msg.data
        self.get_logger().info(f"[DONANIM] /dev/ttyUSB0 üzerinden karta giden ham sinyal -> {komut}")

def main(args=None):
    rclpy.init(args=args)
    node = MotorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Motor düğümü kapatiliyor...")
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()