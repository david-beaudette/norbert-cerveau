#!/usr/bin/env python

from time import sleep
from picamera import PiCamera

import rospy
from sensor_msgs.msg import Image, CameraInfo
import camera_info_manager

import numpy as np
import cv2

class PiCameraNode:
    def __init__(self,
                 width,
                 height,
                 frame_id):
        
        self.picamera = PiCamera()
        self.picamera.resolution = (width, height)
        
        self.picamera.start_preview()
        
        # Camera warm-up time
        sleep(0.75)
        #self.picamera.capture('foo0.75.jpg')
        
        # Initialise ros node
        rospy.init_node("norbertcam")
        self.pub = rospy.Publisher("image_raw",
                                   Image, self, queue_size=1)
        self.caminfo_pub = rospy.Publisher("camera_info",
                                           CameraInfo, self, queue_size=1)

        #while not rospy.is_shutdown():
        #    self.picamera.
        #    rate.sleep()

    def publishMsg(self):
        '''Publish jpeg image as a ROS message'''
        self.msg = CompressedImage()
        self.msg.header.stamp = rospy.Time.now()
        self.msg.header.frame_id = self.axis.frame_id
        self.msg.format = "jpeg"
        self.msg.data = self.img
        self.pub.publish(self.msg)

    def publishCameraInfoMsg(self):
        '''Publish camera info manager message'''
        cimsg = self.axis.cinfo.getCameraInfo()
        cimsg.header.stamp = self.msg.header.stamp
        cimsg.header.frame_id = self.axis.frame_id
        cimsg.width = self.axis.width
        cimsg.height = self.axis.height
        self.caminfo_pub.publish(cimsg)
        
if __name__ == '__main__':
    try:
        PiCameraNode(1024, 768, 'CAM')
        
    except rospy.ROSInterruptException:
        pass
    
    