class RobotState:
    # Robotun içinde bulunabileceği tüm olası durumlar
    IDLE = "BEKLEMEDE"
    SEARCHING = "ARAMA_YAPIYOR"
    TRACKING = "HEDEFE_KILITLENDI"
    ERROR = "HATA_DURUMU"

class StateMachine:
    def __init__(self):
        self.current_state = RobotState.IDLE
        print(f"[CORE] Durum Makinesi Baslatildi. Ilk Durum: {self.current_state}")

    def update_state(self, vision_status, system_health="OK"):
        # 1. Öncelik: Sistemde fiziksel bir arıza varsa her şeyi durdur
        if system_health != "OK":
            self.current_state = RobotState.ERROR
            return self.current_state

        # 2. Durumlar arası geçiş mantığı
        if self.current_state == RobotState.IDLE:
            # Sistem başlatıldıktan sonra otomatik olarak aramaya başla
            self.current_state = RobotState.SEARCHING

        elif self.current_state == RobotState.SEARCHING:
            # Eğer kamera bir nesne bulduysa takip moduna geç
            if vision_status == "nesne_bulundu":
                self.current_state = RobotState.TRACKING

        elif self.current_state == RobotState.TRACKING:
            # Eğer nesne kameranın açısından çıktıysa tekrar aramaya dön
            if vision_status == "nesne_kayip":
                self.current_state = RobotState.SEARCHING

        return self.current_state