#%%
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
import os
from datetime import datetime

#Class made to reduce the quality of given images, to create more images for a dataset

#%%
def Rotator(image):
    rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return rotated 

#%%
def Blur(image, filter):
    blur = cv2.blur(image, (filter, filter))
    return blur

#%%
def Noise(noise_typ,image):

    if noise_typ == "0": #GAUSSIAN

        row,col,ch= image.shape
        mean = 0
        var = 0.1
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,(row,col,ch))
        gauss = gauss.reshape(row,col,ch)
        noisy = image + gauss

        return noisy

    elif noise_typ == "1": #SALT AND PEPPER

        row,col,ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                for i in image.shape]
        out[coords] = 0

        return out

    elif noise_typ == "2": #POISSON

        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)

        return noisy

    elif noise_typ == "3": #SPECKLE

        row,col,ch = image.shape
        gauss = np.random.randn(row,col,ch)
        gauss = gauss.reshape(row,col,ch)        
        noisy = image + image * gauss

        return noisy

#%%
def Preprocess(image):

    temp1 = image
    w = random.randint(0,1999)
    filter = random.randint(1, 5)
    randomiser = random.randint(1,3)
    noisefactor = random.randint(0,3)

    for i in range(10):
        if randomiser == 1:
            temp1 = Rotator(image)
        elif randomiser == 2:
            temp1 = Blur(image, filter)
        elif randomiser == 3:
            temp1 = Noise(noisefactor, image)

        gray = cv2.cvtColor(temp1, cv2.COLOR_BGR2GRAY)
        final = cv2.resize(gray, (1250, 1250), interpolation = cv2.INTER_AREA)

        print("Finished Image: ", i)
        cv2.imwrite("Meddled/dataset" + str(i) + str(w) + ".png", final, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    return final

#%%
start = datetime.now()
for x in os.listdir("Images"):

    image = cv2.imread("Images/" + x, cv2.COLOR_BGR2GRAY)
    try:
        Preprocess(image)
    except Exception as e:
        print(str(e))
    print("Finished: ", x)

end = datetime.now()
print("Finished in: ", (end-start))


# %%
