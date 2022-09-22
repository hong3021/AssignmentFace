import os
import cv2
import numpy as np
from PIL import Image


names = []
path = []


def train_photo():
    # Get the names of all the users


    # Get the path to all the images

    for image in os.listdir("../../Train"):
        path_string = os.path.join("../../Train", image)
        path.append(path_string)

    faces = []
    ids = []

    # For each image create a numpy array and add it to faces list
    for img_path in path:
        image = Image.open(img_path).convert("L")

        imgNp = np.array(image, "uint8")
        faces.append(imgNp)
        # print(path)
        # id = int(img_path.split('/')[3].split('_')[1])
        id = int(img_path.split('\\')[1].split('_')[1])
        ids.append(id)

    ids = np.array(ids)

    print("[INFO] Created faces and names Numpy Arrays")
    print("[INFO] Initializing the Classifier")

    # Make sure contrib is installed
    # The command is pip install opencv-contrib-python

    # Call the recognizer

    trainer = cv2.face.LBPHFaceRecognizer_create()
    # Give the faces and ids numpy arrays
    trainer.train(faces, ids)
    # Write the generated model to a yml file
    trainer.write("training.yml")

    print("[INFO] Training Done")


train_photo()
