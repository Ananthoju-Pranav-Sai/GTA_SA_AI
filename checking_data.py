import numpy as np
import cv2

train_data = np.load('train_data-3.npy',allow_pickle=True)

for data in train_data:
    img = data[0]
    print(img.shape)
    key = data[1]
    cv2.imshow('test',img)
    print(key)
    if(cv2.waitKey(25) & 0xFF == ord('q')):
        cv2.destroyAllWindows()
        break