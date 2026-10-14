#!/usr/bin/env python3 
import rclpy  
from rclpy.node import Node 
from geometry_msgs.msg import Point 
import math 
from std_msgs.msg import Float64  
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import numpy as np
import threading 


class MonitorNode(Node):
    def __init__(self):
        super().__init__("monitor_node") 
        self.plot_x = 0.0 
        self.plot_y = 0.0 
        self.trace_x = []
        self.trace_y = []

        #Making a subscriber from position node to get the positions being plot to show them in live plotting of the bots positions 
        self.subscriber_ = self.create_subscription(Point , "/position" , self.position_retriver ,10)


        #Making a timer to show me plot every 0.2 sec so ik where the bot is 
        # self.plot_timer_ = self.create_timer(0.2 , self.plotter_animation ) # We define this continuity in main function so it doesnt clasehs with spin 


    def position_retriver(self , msg):
        self.plot_x = msg.x 
        self.plot_y = msg.y 
        self.trace_x.append(msg.x)
        self.trace_y.append(msg.y)

        self.get_logger().info(f"We got the plotting points X = {self.plot_x} , Y = {self.plot_y} ")


    def animation(self , i):
        x_val = self.plot_x 
        y_val = self.plot_y

        plt.cla()
        plt.xlim(-100 , 100)
        plt.ylim(-100 , 100)
        plt.plot(self.trace_x, self.trace_y, '-', color="blue")
        plt.plot(x_val , y_val , "o" , markersize = 15 , color = "red")

    # def plotter_animation(self):
    #     ani = FuncAnimation(plt.gcf() , self.animation , interval = 200)
    #     plt.tight_layout()
    #     plt.show()


def main(args = None):
    rclpy.init(args = args)
    node = MonitorNode()

    threading.Thread(target= rclpy.spin , args=(node , ) , daemon = True).start()


    fig = plt.figure()
    ani = FuncAnimation(fig , node.animation , interval = 200)
    plt.show()


    rclpy.shutdown()


if __name__ == "__main__":
    main()