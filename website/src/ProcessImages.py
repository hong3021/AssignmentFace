import cv2
import numpy as np
import os
from pathlib import Path
import uuid

names = []
path = []
# Define a sharpening kernel
shrp_kernel = np.array([[0,  -1,  0],
                   [-1,  5, -1],
                   [0,  -1,  0]])


def process_photo():
    # Get the names of all the users
    for users in os.listdir("../../dataset"):
        names.append(users)

    # # Get the path to all the images
    for name in names:
        for image in os.listdir("../../dataset/{}".format(name)):
            path_string = os.path.join("../../dataset/{}".format(name), image)
            path.append(path_string)

    # For each image create a numpy array and add it to faces list
    for img_path in path:
        image = cv2.imread(img_path)
        image_sharpened = cv2.filter2D(src=image, ddepth=-1, kernel=shrp_kernel)
        image_blurred = cv2.blur(src=image_sharpened, ksize=(7, 7))
        image_convert = cv2.convertScaleAbs(image_blurred, alpha=0.6, beta=20)
        grayImg = cv2.cvtColor(image_convert, cv2.COLOR_BGR2GRAY)
        Path("../../Train/").mkdir(parents=True, exist_ok=True)
        id = img_path.split('\\')[1].split('_')[1]
        cv2.imwrite("../../Train/recon-train_{}_{}.jpg".format(id,str(uuid.uuid1())), grayImg)


process_photo()







