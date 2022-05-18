import numpy as np
import cv2
import matplotlib.pyplot as plt

for i in range(1,12):
    train_data = np.load(f'train_data-{i}.npy',allow_pickle=True)

    for data in train_data:
        img = data[0]
        print(img.shape)
        key = data[1]
        plt.imshow(img)
        plt.show()
        exit()
        # cv2.imshow('test',img)
        # print(key)
        # if(cv2.waitKey(25) & 0xFF == ord('q')):
        #     cv2.destroyAllWindows()
        #     break