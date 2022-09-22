import cv2
import os

faceCascade = cv2.CascadeClassifier("website/src/haarcascade_frontalface_default.xml")
# Call the trained model yml file to recognize faces
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("website/src/training.yml")

with open('website/src/namelist.txt', 'r') as file:
    names = file.read().splitlines()


class Video(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frames(self):
        detectedID = -1
        ret, frame = self.video.read()
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray_image, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confident = recognizer.predict(gray_image[y: y + h, x: x + w])
            if id and confident >= 63.5:
                detectedID = id
                cv2.putText(
                    frame,
                    names[id - 1],
                    (x, y - 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    1,
                    cv2.LINE_AA,
                )
            else:
                cv2.putText(
                    frame,
                    "Unknown",
                    (x, y - 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA,
                )

        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes(), detectedID

