
import numpy as np
import pyautogui
import cv2

def screenshot(with_pil = False):
    im = pyautogui.screenshot()
    frame_rgb = np.array(im)
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    return frame_bgr if not with_pil else (frame_bgr, im)

def locate(img_small, img_big, max_err=1):
    res = cv2.matchTemplate(img_small, img_big, cv2.TM_SQDIFF_NORMED)
    mn,_,mnLoc,_ = cv2.minMaxLoc(res)
    
    if(mn < max_err):
        return True, mnLoc, mn
    else: 
        return False, None, mn
