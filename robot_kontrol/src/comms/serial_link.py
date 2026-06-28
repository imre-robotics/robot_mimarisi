class HardwareLink:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        print(f"[COMMS] Baglanti parametreleri ayarlandi: {port} at {baudrate}")

    def baglan(self):
        print(f"[COMMS] {self.port} portu üzerinden donanima baglanildi.")

    def komut_gonder(self, komut):
        print(f"[COMMS] Seri porttan giden ham veri -> {komut}")

    def baglantiyi_kes(self):
        print("[COMMS] Seri port baglantisi güvenli bir sekilde kapatildi.")