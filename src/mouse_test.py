
import pyautogui
import cv2
import libs.cv2_util as cv2_util

from imutils.object_detection import non_max_suppression
import numpy as np

img = np.ones((100,200))
cv2.imshow("tmp_img",img)

p1 = None

try:
    while(True):
        key = cv2.waitKey(10)
        if(key ==ord('q')): break

        if(key == ord(' ')):
            if(p1 != None):
                p2 = pyautogui.mouseinfo.position()
                x1 = min(p1[0], p2[0])
                x2 = max(p1[0], p2[0])
                y1 = min(p1[1], p2[1])
                y2 = max(p1[1], p2[1])
                print([x1,y1, x2,y2])
                p1 = None
            else:
                p1 = pyautogui.mouseinfo.position()

except KeyboardInterrupt:
    pass
