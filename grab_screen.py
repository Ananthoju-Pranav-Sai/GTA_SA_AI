import numpy as np
from PIL import ImageGrab
import cv2
import time
from direct_keys import PressKey,ReleaseKey,W,A,S,D

def draw_lines(img,lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]), [255,255,255], 3)
    except:
        pass

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,vertices,255)
    masked = cv2.bitwise_and(img,mask)
    return masked

def preprocess_img(img):
    pro_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    pro_img = cv2.Canny(pro_img,threshold1=30,threshold2=150)
    pro_img = cv2.GaussianBlur(pro_img, (3,3), 0 )
    vertices = np.array([[10,500],[10,300], [300,280], [500,280], [800,300], [800,500]], np.int32)
    pro_img = roi(pro_img, [vertices])
    lines = cv2.HoughLinesP(pro_img, 1, np.pi/180, 180, 20, 15)
    draw_lines(pro_img,lines)
    return pro_img

def main():
    last_time = time.time()
    while(True):
        screen = np.array(ImageGrab.grab(bbox=(10,40,800,600)))
        screen = preprocess_img(screen)
        print(f'Loop took {time.time()-last_time} seconds')
        last_time = time.time()
        cv2.imshow('window',screen)
        if(cv2.waitKey(25) & 0xFF == ord('q')):
            cv2.destroyAllWindows()
            break

main()