import os
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.7/bin")
from concurrent.futures import process
import cv2, time, random
import numpy as np
from grab_screen import grab_screen
from getkeys import key_check
from collections import deque, Counter
from model import inception_v3 as googlenet
from direct_keys import PressKey, ReleaseKey, W, A, S, D

GAME_WIDTH = 800
GAME_HEIGHT = 600

how_far_remove = 800
rs = (20, 15)
log_len = 25

motion_req = 800
motion_log = deque(maxlen = log_len)

WIDTH = 281
HEIGHT = 791
LR = 1e-3
EPOCHS = 10

choices = deque([], maxlen = 5)
hl_hist = 250
choice_hist = deque([], maxlen = hl_hist)

t_time = 0.25

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

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)


def left():
    if random.randrange(0, 3) == 1:
        PressKey(W)
    else:
        ReleaseKey(W)
    PressKey(A)
    ReleaseKey(S)
    ReleaseKey(D)
##    ReleaseKey(S)


def right():
    if random.randrange(0, 3) == 1:
        PressKey(W)
    else:
        ReleaseKey(W)
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(S)


def reverse():
    PressKey(S)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)


def no_keys():
    if random.randrange(0, 3) == 1:
        PressKey(W)
    else:
        ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)


# model = googlenet(WIDTH, HEIGHT, 3, LR, output = 5)
model = googlenet(281,791,output=5,lr=LR)
MODEL_NAME = 'fpp_training_data/v29'
model.load(MODEL_NAME)

print('Loaded Model succesfully')

def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    mode_choice = 0

    screen = grab_screen(region = (10, 40, GAME_WIDTH, GAME_HEIGHT))
    screen = process_img(screen)

    while(True):
        if not paused:
            print('entered')
            screen = grab_screen(region = (10, 40, GAME_WIDTH, GAME_HEIGHT))
            screen = process_img(screen)

            prediction = model.predict([screen.reshape(281,791, 1)])[0]
            prediction = np.array(prediction)
            print(prediction)
            mode_choice = np.argmax(prediction)

            if mode_choice == 0:
                straight()
                choice_picked = 'straight'
            elif mode_choice == 1:
                reverse()
                choice_picked = 'reverse'
            elif mode_choice == 2:
                left()
                choice_picked = 'left'
            elif mode_choice == 3:
                right()
                choice_picked = 'right'
            elif mode_choice == 4:
                no_keys()
                choice_picked = 'nokeys'

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)

if __name__ == "__main__":
    main()