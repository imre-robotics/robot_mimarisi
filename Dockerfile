# Temel işletim sistemi olarak Ubuntu 22.04 kullanıyoruz
# Temel imaj olarak içinde ROS 2 Humble kurulu olan resmi sürümü alıyoruz
FROM ros:humble-ros-base

# Gerekli ek araçları ve Python pip paketlerini kuruyoruz
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Konteyner her açıldığında ROS 2 çevre değişkenlerini otomatik olarak yükle (Source et)
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

CMD ["/bin/bash"]

# Gerekli temel paketleri ve derleyicileri kuruyoruz
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinimizi belirliyoruz (Konteynerin içindeki ana klasörümüz)
WORKDIR /app

# Terminal açıldığında bizi karşılayacak komut
CMD ["/bin/bash"]
