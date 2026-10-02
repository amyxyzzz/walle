#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

# import the message type to use
from std_msgs.msg import Int64, Bool
from geometry_msgs.msg import Twist



class constantControl(Node):
    def __init__(self) -> None:
				# initialize base class (must happen before everything else)
        super().__init__("constantcontrol")  # initialize base class
				
				# a heartbeat counter
		# 		self.cc_counter = 0

		# 		# create publisher with
		# 		#   self.create_publisher(<msg type>, <topic>, <qos>)
        self.cc_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        
        # create a timer
				#   self.create_timer(<second>, <callback>)
        self.cc_timer = self.create_timer(0.2, self.cc_callback)
        self.kill_sub = self.create_subscription(Bool, "/kill", self.kill_callback, 10)

				# create subscription with
				#   self.create_subscription(<msg type>, <topic>, <callback>, <qos>)
        # self.motor_sub = self.create_subscription(Bool, "/health/motor",
        #                                           self.health_callback, 10)
    def cc_callback(self) -> None:
        
        #self.get_logger().info("sending constant control... ")
		# """ heartbeat callback triggered by the timer """
        # construct heartbeat message
        msg = Twist()  # 0 initialize everything by default
        msg.linear.x = 1.0  # set this to be the linear velocity
        msg.angular.z = .5# set this to be the angular velocity
        # msg.data = self.hb_counter

        # # publish heartbeat counter
        self.cc_pub.publish(msg)

		# 		# counter increment
        # self.hb_counter += 1

    # def health_callback(self, msg: Bool) -> None:
    #     """ sensor health callback triggered by subscription """
    #     if not msg.data:
    #         self.get_logger().fatal("Heartbeat stopped")
    #         self.hb_timer.cancel()
    def kill_callback(self, msg):
        if msg.data:
            self.cc_timer.cancel()
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.cc_pub.publish(stop_msg)


if __name__ == "__main__":
    rclpy.init()        # initialize ROS2 context (must run before any other rclpy call)
    node = constantControl()  # instantiate the heartbeat node
    rclpy.spin(node)    # Use ROS2 built-in schedular for executing the node
    rclpy.shutdown()    # cleanly shutdown ROS2 context