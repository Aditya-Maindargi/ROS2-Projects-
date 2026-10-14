#!usr/bin/env python3 
import rclpy 
from rclpy.node import Node  
from geometry_msgs.msg import Point  
from robot_interface.srv import MoveTo
from std_msgs.msg import Float64 



class DesitnationNode(Node):
    def __init__(self):
        super().__init__("destination_node")  
        #Destination Variables 
        self.x , self.y = 0.0 , 0.0 
        self.speed_request = 0.0 

        #Variables for server 
        self.srv_ = self.create_service(MoveTo , "/move_to" , self.callback_move_to)
        self.speed_publisher_ = self.create_publisher(Float64 , "/speed" , 10)

        #Making a topic 
        self.publisher_ = self.create_publisher(Point , "/destination" , 10)
        self.timer_ = self.create_timer(0.2 , self.callback_destination) 
        self.get_logger().info("The Destination will be starting to get provided once robot moves !")





        

    def callback_destination(self):
        msg = Point()
        msg.x = float(self.x)
        msg.y = float(self.y)
        msg.z = 0.0  
        self.publisher_.publish(msg)
        
        #For speed 
        speed_msg = Float64()
        speed_msg.data = float(self.speed_request)
        self.speed_publisher_.publish(speed_msg)

    def callback_move_to(self , request , response):
        self.x = request.x 
        self.y = request.y 
        self.speed_request = request.speed

        self.get_logger().info(f"New Target Recieved  X = {self.x} and Y = {self.y} & Speed = {self.speed_request} ")
        response.success = True 
        return response
        


def main(args = None):
    rclpy.init(args = args)
    node = DesitnationNode()
    rclpy.spin(node)
    rclpy.shutdown() 


if __name__ == "__main__":
    main()