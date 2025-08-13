# Smart Cane for the Visually Impaired

An assistive device powered by SLAM, object detection, and sensor fusion to help visually impaired users navigate indoor environments safely.

## 📌 Project Description

This project aims to build a smart walking cane that performs localization and mapping (SLAM), real-time obstacle detection, and provides feedback through vibration or voice. It uses:
- **RTAB** for visual-inertial SLAM
- **YOLOv11** for object detection
- **Ultrasonic, ToF, and IMU sensors** for obstacle detection
- **Speaker and vibration motors** for assistive feedback

## 🧠 Key Features

- Localization and mapping
- Obstacle detection
- Path planning and navigation cues
- Assistive feedback via vibration and TTS (text-to-speech)

## 🛠️ Tech Stack

- **Hardware**: Raspberry Pi 4B, IMU, Ultrasonic sensors, ToF, camera, Laptop
- **Software**: Python, YOLOv8, Linux (Bookworm)
- **Libraries**: OpenCV, NumPy, PyTorch, rclpy

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/dilly-cally/project25.git
cd project25
