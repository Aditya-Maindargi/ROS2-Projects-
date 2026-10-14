#!/usr/bin/env python3 
import rclpy  
from rclpy.node import Node 
from geometry_msgs.msg import Point 
import math 
from std_msgs.msg import Float64 



class PositionNode(Node): 
    def __init__(self):
        super().__init__("position_node") 

        
        self.x,self.y = 0.0,0.0
        self.target_x,self.target_y = 0.0,0.0
        self.speed = 0.0
        self.dt = 0.2 

        #Making a subscriber to get info from destination node 
        self.subscriber_ = self.create_subscription(Point,"/destination",self.callback_destination,10)
        self.speed_subscriber_ = self.create_subscription(Float64 , "/speed" , self.callback_speed , 10)

        #Making a publisher 
        self.publisher_ = self.create_publisher(Point,"/position",30) 

        self.timer_ = self.create_timer(0.2,self.callback_position)
        self.get_logger().info("Position Updates will arrive soon !")




    def callback_speed(self,msg):
        self.speed = msg.data 


    def callback_destination(self,msg):
        self.target_x = msg.x 
        self.target_y = msg.y 

        self.get_logger().info(f"The Target location are X = {self.target_x},Y = {self.target_y} & the speed is {self.speed}")


    # Updating Coordinates function 
    def position_update(self):
        step_len = self.speed * self.dt

        dx = self.target_x - self.x
        dy = self.target_y - self.y

        d = math.hypot(dx, dy)

      
        if d <= step_len:
            self.x = self.target_x
            self.y = self.target_y
            return

        # Move towards the target
        self.x += (dx / d) * step_len
        self.y += (dy / d) * step_len


    def callback_position(self): 

        self.position_update()

        msg = Point() 
        msg.x = float(self.x)
        msg.y = float(self.y)
        msg.z = 0.0 
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PositionNode()
    rclpy.spin(node) 
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()