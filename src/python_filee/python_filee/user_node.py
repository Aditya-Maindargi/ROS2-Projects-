#!/usr/bin/env python3 
import rclpy 
from rclpy.node import Node 
from robot_interface.srv import MoveTo
from geometry_msgs.msg import Point  
from functools import partial



class UserNode(Node):
    def __init__(self):
        super().__init__("user_node")
        self.client_ = self.create_client(MoveTo , "/move_to")
        self.client_.wait_for_service(timeout_sec = 0.1)
        self.user_x = 0.0
        self.user_y = 0.0
        self.user_speed = 0.0 


    def user_request(self):
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for the Server.......")

        self.user_x = float(input("Enter the X coordinate to move to : "))
        self.user_y = float(input("Enter the Y coordinate to move to : "))
        self.user_speed = float(input("Enter the required speed : "))

        request = MoveTo.Request()
        request.x = self.user_x 
        request.y = self.user_y 
        request.speed = self.user_speed 


        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_add_two_ints,request=request))

    def callback_call_add_two_ints(self, future ,request ):
        response = future.result()
        self.get_logger().info(str(request.x) + " + " + str(request.y) + " = " + str(response.success))


def main(args = None):
     rclpy.init(args = args)
     node = UserNode()
     node.user_request()
     rclpy.spin(node)
     rclpy.shutdown()



if __name__ == "__main__":
    main()       

