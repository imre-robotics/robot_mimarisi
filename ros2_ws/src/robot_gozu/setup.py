from setuptools import setup
import os
from glob import glob

package_name = 'robot_gozu'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # İŞTE YENİ EKLENEN LAUNCH SATIRI:
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='main',
    maintainer_email='main@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'kamera_servisi = robot_gozu.kamera_node:main',
            'beyin_servisi = robot_gozu.beyin_node:main',
            'motor_servisi = robot_gozu.motor_node:main'
        ],
    },
)
