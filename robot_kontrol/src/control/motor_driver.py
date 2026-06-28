class MotorController:
    def __init__(self):
        print("[CONTROL] Motor kontrol birimi aktif (PID/Kinematik hazir).")

    def hiz_hesapla(self, hedef):
        # Donanıma gönderilecek hız profilini hesaplayan matematiksel alan
        hesaplanan_hiz = hedef * 0.95
        print(f"[CONTROL] Hedef: {hedef} -> Hesaplanan Motor Hizi: {hesaplanan_hiz}")
        return hesaplanan_hiz