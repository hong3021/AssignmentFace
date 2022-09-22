import cv2
import numpy as np
from pathlib import Path
import time
import os
import uuid

# Initialize the classifier
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
shrp_kernel = np.array([[0,  -1,  0],
                   [-1,  5, -1],
                   [0,  -1,  0]])


def save_image(image, user_name, img_count):
    # Create a folder with the name as userName

    Path("../../dataset/{}".format(user_name)).mkdir(parents=True, exist_ok=True)
    userid = len(os.listdir("../../dataset"))
    # Save the images inside the previously created folder

    cv2.imwrite("../../dataset/{}/{}_{}_{}.jpg".format(user_name, user_name, userid, img_count), image)

    print(f"[INFO] Image has been saved in folder : {user_name}")


def process_photo(user_name):
    path = []
    for image in os.listdir("../../dataset/{}".format(user_name)):
        path_string = os.path.join("../../dataset/{}".format(user_name), image)
        path.append(path_string)
    for img_path in path:
        image = cv2.imread(img_path)

        image_sharpened = cv2.filter2D(src=image, ddepth=-1, kernel=shrp_kernel)
        image_blurred = cv2.blur(src=image_sharpened, ksize=(5, 5))
        grayImg = cv2.cvtColor(image_blurred, cv2.COLOR_BGR2GRAY)
        Path("../../Train/").mkdir(parents=True, exist_ok=True)
        id = img_path.split('\\')[1].split('_')[1]
        cv2.imwrite("../../Train/recon-train_{}_{}.jpg".format(id, str(uuid.uuid1())), grayImg)


class Capture:
    def __init__(self):
        # Start the video camera
        self.video = cv2.VideoCapture(0)
        self.imgCount = 8
        self.count = 1
        print("Enter the name of the person: ")
        self.userName = input()

    def capture_photo(self):
        print("[INFO] Video Capture is now starting please stay still...")
        time.sleep(3)
        file = open('namelist.txt', 'a')
        file.writelines(self.userName + '\n')
        file.close()

        while True:
            # Capture the frame/image
            _, img = self.video.read()

            # Copy the original Image
            originalImg = img.copy()

            # Get the gray version of our image
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Get the coordinates of the location of the face in the picture
            faces = faceCascade.detectMultiScale(gray_img,
                                                 scaleFactor=1.2,
                                                 minNeighbors=5,
                                                 minSize=(50, 50))

            # Draw a rectangle at the location of the coordinates
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                coords = [x, y, w, h]

            # Show the image
            cv2.imshow("Identified Face", img)

            # Wait for user keypress
            key = cv2.waitKey(1) & 0xFF

            # Check if the pressed key is 'k' or 'q'
            if key == ord('s'):
                # If count is less than 5 then save the image
                if self.count <= self.imgCount:
                    roi_img = originalImg[coords[1] : coords[1] + coords[3], coords[0] : coords[0] + coords[2]]
                    save_image(roi_img, self.userName, self.count)
                    self.count += 1
                else:
                    break
            # If q is pressed break out of the loop
            elif key == ord('q'):
                break

        print("[INFO] Dataset has been created for {}".format(self.userName))
        process_photo(self.userName)
        # Stop the video camera
        self.video.release()
        # Close all Windows
        cv2.destroyAllWindows()


Capture().capture_photo()


