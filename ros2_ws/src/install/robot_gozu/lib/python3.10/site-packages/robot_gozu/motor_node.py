import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist  # Motor sürücü artık Twist dinliyor

class MotorNode(Node):
    def __init__(self):
        super().__init__('motor_node')
        self.abonelik = self.create_subscription(
            Twist, '/motor_komutlari', self.motor_callback, 10)
        self.get_logger().info("=== [ROS 2] Motor Sürücü Düğümü (Twist Uyumlu) Aktif ===")

    def motor_callback(self, msg):
        # Dönüş vektörlerini alıp gerçek fiziksel sürücüye aktarıyoruz
        ileri_hiz = msg.linear.x
        donus_hizi = msg.angular.z
        
        self.get_logger().info(
            f"[DONANIM SÜRÜCÜ] Seri Port -> İleri Hız: {ileri_hiz} m/s | Dönüş: {donus_hizi} rad/s")

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