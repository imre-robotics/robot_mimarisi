import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class AcilStopNode(Node):
    def __init__(self):
        super().__init__('acil_stop_node')
        # Tüm sistemi durduracak olan yüksek öncelikli topiği açıyoruz
        self.yayinci = self.create_publisher(String, '/acil_durum', 10)
        self.get_logger().warn("=== [GÜVENLİK] E-Stop Düğümü Aktif ===")
        
        # Test için saniyede bir kez sistemi kilitleme sinyali basacak
        self.timer = self.create_timer(1.0, self.guvenlik_yayinla)

    def guvenlik_yayinla(self):
        msg = String()
        msg.data = "STOP"
        self.yayinci.publish(msg)
        self.get_logger().error("[!KIRMIZI BUTON!] Sisteme STOP emri basiliyor!")

def main(args=None):
    rclpy.init(args=args)
    node = AcilStopNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Güvenlik sistemi kapaniyor...")
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()