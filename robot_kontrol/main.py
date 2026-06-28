import time
import sys
import random

# Kendi modüllerimizi çağırıyoruz
from src.vision.camera_handler import Camera
from src.control.motor_driver import MotorController
from src.comms.serial_link import HardwareLink
from src.core.state_machine import StateMachine, RobotState

def ana_dongu():
    print("=========================================")
    print("     IMRE ROBOTICS SYSTEM INTERFACES     ")
    print("=========================================\n")
    
    # Alt sistemleri ve Zekayı (FSM) ayağa kaldırıyoruz
    kamera = Camera()
    motorlar = MotorController()
    donanim = HardwareLink(port="/dev/ttyUSB0", baudrate=115200)
    beyin = StateMachine()
    
    donanim.baglan()
    print("\n--- Sistem Canli Döngüye Geciyor (Cikis icin Ctrl+C) ---\n")
    
    sayac = 0
    try:
        while sys.platform == "linux" or sys.platform == "linux2":
            sayac += 1
            print(f"\n[DÖNGÜ #{sayac}]")
            
            # 1. GÖZLER: Kameradan veri oku (Burada rastgelelik ekledik)
            kamera_durumu = random.choice(["nesne_bulundu", "nesne_bulundu", "nesne_kayip"])
            print(f"[VISION] Kamera okumasi: {kamera_durumu}")
            
            # 2. BEYİN: Kamera verisine göre robotun yeni durumuna karar ver
            mevcut_durum = beyin.update_state(vision_status=kamera_durumu)
            print(f"[CORE] Aktif Durum: {mevcut_durum}")
            
            # 3. KASLAR VE İLETİŞİM: Beynin kararına göre motorları sür
            if mevcut_durum == RobotState.TRACKING:
                hiz = motorlar.hiz_hesapla(hedef=100)
                donanim.komut_gonder(f"M_SPEED:{hiz}")
                
            elif mevcut_durum == RobotState.SEARCHING:
                print("[CONTROL] Nesne araniyor... Kendi etrafinda yavasca dönülüyor.")
                donanim.komut_gonder("M_SPEED:30, TURN:RIGHT")
                
            elif mevcut_durum == RobotState.IDLE:
                print("[CONTROL] Sistem beklemede. Motorlar stop.")
                donanim.komut_gonder("M_SPEED:0, TURN:CENTER")
            
            time.sleep(2) 
            
    except KeyboardInterrupt:
        print("\n[UYARI] Kullanici kesmesi algilandi! Sistem kapatiliyor...")
        donanim.baglantiyi_kes()
        print("=========================================")

if __name__ == "__main__":
    ana_dongu()