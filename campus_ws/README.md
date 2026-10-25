# Autonomous Campus Delivery Robot Simulation (ROS 2)

An autonomous mobile robot simulation built in ROS 2 Humble and Gazebo designed to perform multi-point waypoint navigation across a custom campus environment.

## 🛠️ Tech Stack & Tools
* **Robotics Framework:** ROS 2 Humble
* **Simulation:** Gazebo, RViz2
* **Navigation Stack:** Navigation2 (Nav2), SLAM Toolbox
* **Language:** Python

---

## 📌 Project Overview
This project simulates an autonomous delivery robot capable of navigating between mapped campus locations. It features custom Python navigation logic that publishes real-time status updates and telemetry data to the `/delivery_status` topic.

---

## 🚀 How to Build and Run

1. Clone this repository into the `src` directory of your ROS 2 workspace:
   ```bash
   cd ~/ros2_ws/src
   git clone [https://github.com/ThusharAnchan/campus-delivery-robot-ros2.git](https://github.com/ThusharAnchan/campus-delivery-robot-ros2.git)
