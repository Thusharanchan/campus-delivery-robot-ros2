#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import time

def create_pose_stamped(navigator, x, y, z):
    """Helper function to format coordinates for Nav2."""
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = float(x)
    pose.pose.position.y = float(y)
    pose.pose.position.z = float(z)
    pose.pose.orientation.w = 1.0
    return pose

def main():
    rclpy.init()
    
    
    status_node = rclpy.create_node('delivery_status_publisher')
    status_pub = status_node.create_publisher(String, '/delivery_status', 10)
    
    def publish_status(msg_text):
        """Helper function to publish to the topic and print to terminal."""
        msg = String()
        msg.data = msg_text
        status_pub.publish(msg)
        print(f"[TOPIC: /delivery_status] {msg_text}")

    
    navigator = BasicNavigator()
    navigator.waitUntilNav2Active()

    
    locations = {
        'home': create_pose_stamped(navigator, 0.002286958, 0.000004676, 0.007810707),
        'hod cabin': create_pose_stamped(navigator, -3.928545897, 3.084161974, 0.007861815),
        'faculty cabin': create_pose_stamped(navigator, -3.785314959, 4.649169547, 0.007853873),
        'admin block': create_pose_stamped(navigator, -0.676781252, 4.377169872, 0.007841405),
        'store room': create_pose_stamped(navigator, 3.751149348, 6.940635556, 0.007837179),
    }

    publish_status("Campus Delivery Bot Online. Waiting for dispatch instructions...")

    while rclpy.ok():
        print("\n=======================================================")
        print("          CAMPUS MAIL & ITEM DELIVERY SYSTEM           ")
        print("=======================================================")
        print("Available Destinations: 'hod cabin', 'faculty cabin', ")
        print("                        'admin block', 'store room'")
        print("Type 'exit' to shut down.")
        print("-------------------------------------------------------")
        
        target = input("Enter destination: ").strip().lower()

        if target == 'exit':
            publish_status("System shutting down...")
            break
        elif target in locations and target != 'home':
            
            # Start full delivery cycle from dispatch to drop-off
            publish_status(f"Request accepted. Item loaded for {target.upper()}.")
            publish_status(f"Navigating to {target.upper()}...")
            
            navigator.goToPose(locations[target])
            
            while not navigator.isTaskComplete():
                time.sleep(1.0) # Check every second

            result = navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                publish_status(f"ARRIVED at {target.upper()}. Commencing drop-off.")
                time.sleep(3.0) # Simulate drop-off time
                publish_status("Drop-off successful. Returning to HOME/Dispatch Bay.")
                
                navigator.goToPose(locations['home'])
                
                while not navigator.isTaskComplete():
                    time.sleep(1.0)
                    
                if navigator.getResult() == TaskResult.SUCCEEDED:
                    publish_status("Successfully returned to HOME. Ready for next delivery.")
                else:
                    publish_status("[ERROR] Failed to return to HOME.")
            else:
                publish_status(f"[ERROR] Path to {target.upper()} failed or was blocked.")
        elif target == 'home':
            publish_status("Robot is already at the Home/Dispatch bay.")
        else:
            print("[ERROR] Invalid location. Please type a name exactly as listed above.")

    status_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()