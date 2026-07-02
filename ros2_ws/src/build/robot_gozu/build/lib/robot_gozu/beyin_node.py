import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist  # İŞTE YENİ EVRENSEL SİLAHIMIZ!

class BeyinNode(Node):
    def __init__(self):
        super().__init__('beyin_node')
        
        self.kamera_abonelik = self.create_subscription(
            String, '/kamera_durumu', self.kamera_callback, 10)
        self.guvenlik_abonelik = self.create_subscription(
            String, '/acil_durum', self.guvenlik_callback, 10)
        
        # Çıkış Hattımız artık String değil, Twist fırlatıyor!
        self.motor_yayinci = self.create_publisher(Twist, '/motor_komutlari', 10)
        
        self.mevcut_durum = "BEKLEMEDE"
        self.acil_durum_aktif = False
        self.get_logger().info("=== [ROS 2] Beyin Düğümü (Twist Standartlı) Hazir ===")

    def guvenlik_callback(self, msg):
        if msg.data == "STOP":
            self.acil_durum_aktif = True
            self.mevcut_durum = "ACIL_DURUM"
            self.get_logger().fatal("[!!!] E-STOP! HIZ VEKTÖRLERİ SIFIRLANIYOR!")
            
            # Acil durumda tüm hızlar tam sıfır!
            dur_emri = Twist()
            dur_emri.linear.x = 0.0
            dur_emri.angular.z = 0.0
            self.motor_yayinci.publish(dur_emri)

    def kamera_callback(self, msg):
        if self.acil_durum_aktif:
            return

        gelen_veri = msg.data
        if gelen_veri == "nesne_bulundu" and self.mevcut_durum != "HEDEFE_KILITLENDI":
            self.mevcut_durum = "HEDEFE_KILITLENDI"
            self.get_logger().warn(f"[BEYIN] Durum: {self.mevcut_durum}!")
        elif gelen_veri == "nesne_kayip" and self.mevcut_durum != "ARAMA_YAPIYOR":
            self.mevcut_durum = "ARAMA_YAPIYOR"
            self.get_logger().info(f"[BEYIN] Durum: {self.mevcut_durum}.")

        # Hız paketimizi (Twist) oluşturuyoruz
        motor_emri = Twist()
        
        if self.mevcut_durum == "HEDEFE_KILITLENDI":
            motor_emri.linear.x = 1.5  # Saniyede 1.5 metre ileri hız!
            motor_emri.angular.z = 0.0 # Düz git
        elif self.mevcut_durum == "ARAMA_YAPIYOR":
            motor_emri.linear.x = 0.0  # İleri gitme
            motor_emri.angular.z = 0.8 # Saniyede 0.8 radyan hızla kendi etrafında dön
        else:
            motor_emri.linear.x = 0.0
            motor_emri.angular.z = 0.0

        self.motor_yayinci.publish(motor_emri)

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