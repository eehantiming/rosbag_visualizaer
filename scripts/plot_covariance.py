#!/usr/bin/env python3
"""ROS1 node that subcribes to some topic for data and displays a plot for it."""


import logging
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import rospy
from std_msgs.msg import Int64
from nav_msgs.msg import Odometry


class Plotter:
    """Class for listening to data, processing and visualizing them.

    ...

    Attributes
    ----------
    handler : EventHandler
        An injected object that tracks file changes. Access handler.states and handler.goals.
    uav_name : String
        e.g. "uav1" ; "uav2"
    odom_subscriber : rospy.Subscriber
        Subscribes to the odometry output from fastlio and performs callback.
    sess : tf.Session()
        the session with the NN to perform forward inference with.

    Methods
    -------
    inference(event=None)
        Performs forward inference, event being time info passed in by the Timer.
    """
    
    def __init__(self, enable_log=False):
        self.odom_subscriber = rospy.Subscriber("/Odometry", Odometry, self.callback_odometry)
        self.logger = logging.getLogger(__name__)
        self.cov1 = 0.
        self.cov2 = 0.
        self.counter = 0

    def callback_odometry(self, msg):
        self.cov1 = msg.pose.covariance[0]
        self.cov2 = msg.pose.covariance[7]
        # self.logger.info(f"i hear {cov1}!")
    
    def animate(self, i, xs, ys, ax1):
        xs.append(self.counter)
        self.counter += 1
        ys.append(self.cov1)
        
        ax1.clear()
        ax1.plot(xs, ys)
    
        
    def animate2(self, i, xs, ys, ax2):
        xs.append(self.counter)
        ys.append(self.cov2)

        ax2.clear()
        ax2.plot(xs, ys)

    
    
def create_logger():
    logger = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handler)
    return logger

def create_animation(plotter):
    fig = plt.figure()
    #creating a subplot 
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    xs = []
    ys = []
    xs2 = []
    ys2 = []
    ani = animation.FuncAnimation(fig, plotter.animate, fargs=(xs,ys,ax1),interval=500) 
    ani2 = animation.FuncAnimation(fig, plotter.animate2, fargs=(xs2,ys2,ax2),interval=500) 

    plt.show()

    
if __name__ == '__main__':
    rospy.init_node('covariance_plotter')
    # Create module level logger.
    logger = create_logger()
    
    plotter = Plotter(enable_log=True)
    create_animation(plotter)

    rospy.spin()