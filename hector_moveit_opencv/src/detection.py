#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

class TreeDetector(object):

    def __init__(self):

        self.image_sub = rospy.Subscriber("camera/rgb/image_raw", Image, self.camera_callback)
        self.bridge_object = CvBridge()

    def camera_callback(self,data):
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 0, 0])
        upper_red = np.array([36, 255, 255])

        mask = cv2.inRange(hsv, lower_red, upper_red)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel)

        # Contours detection
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        matrix = np.zeros((16, 2))
        i = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 400:
                cv2.drawContours(cv_image, [cnt], 0, (0, 187, 45), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                rectarea = w*h
                if rectarea > 1100:
                    cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(cv_image, "Tree", (x + w + 5, y + 5), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1)
                    matrix[i][0] = x + w/2 #il centro del contorno rilevato coordinata x
                    matrix[i][1] = y + h/2 #il centro del contorno rilevato coordinata y
                    i = i + 1
            if(i==16):
                i = 0
        
        print(matrix)



def main():
    tree_detector_object = TreeDetector()
    rospy.init_node('tree_detector_node', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main()