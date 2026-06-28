import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class BeyinNode(Node):
    def __init__(self):
        super().__init__('beyin_node')
        
        # 1. Giriş Hattı: Kamerayı dinle
        self.abonelik = self.create_subscription(
            String, '/kamera_durumu', self.kamera_callback, 10)
        
        # 2. Çıkış Hattı: Motor düğümüne emir yayınla
        self.motor_yayinci = self.create_publisher(String, '/motor_komutlari', 10)
        
        self.mevcut_durum = "BEKLEMEDE"
        self.get_logger().info("=== [ROS 2] Beyin Düğümü Dinlemeye ve Emir Vermeye Hazir ===")

    def kamera_callback(self, msg):
        gelen_veri = msg.data
        
        # State Machine Mantığı
        if gelen_veri == "nesne_bulundu" and self.mevcut_durum != "HEDEFE_KILITLENDI":
            self.mevcut_durum = "HEDEFE_KILITLENDI"
            self.get_logger().warn(f"[BEYIN] Durum: {self.mevcut_durum}!")
            
        elif gelen_veri == "nesne_kayip" and self.mevcut_durum != "ARAMA_YAPIYOR":
            self.mevcut_durum = "ARAMA_YAPIYOR"
            self.get_logger().info(f"[BEYIN] Durum: {self.mevcut_durum}.")

        # Karara göre motor emir mesajını oluştur ve fırlat
        motor_emri = String()
        if self.mevcut_durum == "HEDEFE_KILITLENDI":
            motor_emri.data = "M_SPEED:95"
        elif self.mevcut_durum == "ARAMA_YAPIYOR":
            motor_emri.data = "M_SPEED:30, TURN:RIGHT"
        else:
            motor_emri.data = "M_SPEED:0"

        self.motor_yayinci.publish(motor_emri)

# --- İŞTE EKSİK OLAN VE SİSTEMİ ATEŞLEYEN KISIM ---
def main(args=None):
    rclpy.init(args=args)
    node = BeyinNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Beyin düğümü kapatiliyor...")
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()