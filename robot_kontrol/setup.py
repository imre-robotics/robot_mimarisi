from setuptools import setup, find_packages

setup(
    name="robot_kontrol",
    version="0.1.0",
    description="Otonom sistemler icin temel kontrol ve sensor paketi",
    author="Mustafa Ali",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # İleride buraya numpy, opencv-python gibi kütüphaneleri yazacağız
    ],
)