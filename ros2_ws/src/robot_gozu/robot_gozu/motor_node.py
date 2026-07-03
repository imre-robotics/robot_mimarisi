import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class CiftYonluDonanimArayuzu(Node):
    def __init__(self):
        super().__init__('motor_node')
        
        # --- TX BÖLÜMÜ (Aşağı Doğru Akış) ---
        # Beyinden gelen otonom hız vektörlerini (Twist) dinleyen kulak
        self.abonelik = self.create_subscription(
            Twist, '/motor_komutlari', self.motor_callback, 10)
            
        # --- RX BÖLÜMÜ (Yukarı Doğru Akış) ---
        # Donanımdan (Enkoderlerden) gelen verileri ayıklayıp üst katmana fırlatacak yayıncı
        self.enkoder_yayinci = self.create_publisher(String, '/enkoder_ham', 10)
        
        # Simülasyon: STM32'den saniyede bir enkoder verisi geliyormuş gibi tetikleme yapıyoruz
        self.rx_timer = self.create_timer(1.0, self.uart_rx_simulasyon)
        
        self.get_logger().info("=== [HAL] Çift Yönlü Donanım Arayüzü (TX/RX) Aktif ===")

    def motor_callback(self, msg):
        # Beynin matematiksel emrini alıp donanım paketine (TX) dönüştürme
        ileri_hiz = msg.linear.x
        donus_hizi = msg.angular.z
        seri_paket_tx = f"<L:{ileri_hiz:.2f},A:{donus_hizi:.2f}>\n"
        self.get_logger().info(f"[UART TX -> DONANIM] Giden Emir: {seri_paket_tx.strip()}")

    def uart_rx_simulasyon(self):
        # 1. HAM RX VERİSİ: Kablodan şu ham bayt dizisinin geldiğini varsayalım
        # Sol tekerlek enkoderi: 1024 tık, Sağ tekerlek enkoderi: 1020 tık dönmüş olsun
        ham_uart_rx = "<E:1024,1020>\n"
        
        # 2. PARSER (AYRIŞTIRICI MANTIĞI)
        # Endüstriyel paketimizin başındaki '<' ve sonundaki '>' şablonunu süzüyoruz
        temiz_veri = ham_uart_rx.strip().replace("<", "").replace(">", "") # Çıktı: "E:1024,1020"
        
        if temiz_veri.startswith("E:"):
            # "E:" kısmını atıp sadece sayıları alıyoruz
            degerler = temiz_veri.split("E:")[1] # Çıktı: "1024,1020"
            sol_enkoder, sag_enkoder = degerler.split(",") # Çıktı: ["1024", "1020"]
            
            # Ayrıştırılan veriyi terminale basıyoruz
            self.get_logger().warn(
                f"[UART RX <- DONANIM] Enkoder Ayristirildi -> Sol: {sol_enkoder} | Sağ: {sag_enkoder}")
            
            # 3. ROS 2 AĞINA FIRLATMA
            # Bu ham sayıları ileride "Odometri (Konum)" hesaplayacak düğümler kullansın diye ağda yayınlıyoruz
            ros_msg = String()
            ros_msg.data = f"SOL:{sol_enkoder},SAG:{sag_enkoder}"
            self.enkoder_yayinci.publish(ros_msg)

def main(args=None):
    rclpy.init(args=args)
    node = CiftYonluDonanimArayuzu()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Donanım Arayüzü kapatiliyor...")
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()