import numpy as np
from grab_screen import grab_screen
import cv2
import time
import os
from getkeys import key_check

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    vertices = np.array([[10,600],[10,300], [310,280], [500,280], [800,300], [800,600]], np.int32)
    processed_img = roi(processed_img, [vertices])
    processed_img = cv2.Canny(processed_img, threshold1=100, threshold2=150)
    processed_img = processed_img[280:600][:]
    return processed_img

# creating one hot encoded label for every key
w = 0
s = 1
a = 2
d = 3
nk = 4    # this represents no key is being pressed

start_value = 1

while True:
    file_name = "fpp_training_data/train_data-{}.npy".format(start_value)

    if (os.path.isfile(file_name)):
        print('File exists, proceeding further ',start_value)
        start_value+=1
    else:
        print('File doesnot exist, starting fresh! ',start_value)
        break
def keys_to_outputs(keys):
    if ('A' in keys):
        return a
    elif ('D' in keys):
        return d
    elif ('W' in keys):
        return w
    elif ('S' in keys):
        return s
    return nk

def main(file_name,start_value):
    train_data = []
    #count down to open the game window
    for i in range(4):
        print(i)
        time.sleep(1)
    
    paused = False
    print('Starting captures')
    size = 100
    count = np.zeros(5)
    n = 0
    while(True):
        if not paused:
            screen = grab_screen(region=(10,40,800,600))
            screen = process_img(screen)

            keys = key_check()
            # print(keys)
            output = [0,0,0,0,0]
            code = keys_to_outputs(keys)
            output[code]=1
            if(count[code]!=size):
                train_data.append([screen,output])
                count[code]+=1
                n+=1
            else:
                continue
            
            print(n,size*5)
            print(count)
            if(n==size*5):
                np.save(file_name,train_data)
                print('Finished saving')
                train_data = []
                start_value +=1
                file_name = f"fpp_training_data/train_data-{start_value}.npy"
                count = np.zeros(5)
                n = 0
    
        keys = key_check()
        if 'P' in keys:
            if paused:
                paused = False
                print('Resumed')
                time.sleep(1)
            else:
                print('Paused')
                paused = True
                time.sleep(1)
        
        if 'Q' in keys:
            exit()

main(file_name,start_value)