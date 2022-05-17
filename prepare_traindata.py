import numpy as np
from grab_screen import grab_screen
import cv2
import time
import os
from getkeys import key_check

# creating one hot encoded label for every key
w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]    # this represents no key is being pressed

start_value = 1

while True:
    file_name = "train_data-{}.npy".format(start_value)

    if (os.path.isfile(file_name)):
        print('File exists, proceeding further ',start_value)
        start_value+=1
    else:
        print('File doesnot exist, starting fresh! ',start_value)
        break
def keys_to_outputs(keys):
    output = [0,0,0,0,0,0,0,0]
    if ('W' in keys and 'A' in keys):
        output = wa
    elif ('W' in keys and 'D' in keys):
        output = wd
    elif ('S' in keys and 'A' in keys):
        output = sa
    elif ('S' in keys and 'D' in keys):
        output = sd
    elif ('W' in keys):
        output = w
    elif ('S' in keys):
        output = s
    elif ('A' in keys):
        output = a
    elif ('D' in keys):
        output = d
    else:
        output = nk
    return output

def main(file_name,start_value):
    train_data = []
    #count down to open the game window
    for i in range(4):
        print(i)
        time.sleep(1)
    
    paused = False
    print('Starting captures')
    while(True):
        if not paused:
            screen = grab_screen(region=(10,40,800,600))

            screen = cv2.resize(screen,(480,270))
            screen = cv2.cvtColor(screen,cv2.COLOR_BGR2GRAY)

            keys = key_check()
            print(keys)
            output = keys_to_outputs(keys)
            train_data.append([screen,output])

            if(len(train_data)%100 == 0):
                print(len(train_data))

                if(len(train_data) == 500):
                    np.save(file_name,train_data)
                    print('Finished saving')
                    train_data = []
                    start_value +=1
                    file_name = f"train_data-{start_value}.npy"
    
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