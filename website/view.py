from flask import Blueprint, render_template, Response, request
from website.camera import Video
import os

views = Blueprint('views', __name__)

global start_cam, face_id, switch, varify, massages
start_cam = True
face_id = []
varify = False

massages = []

with open('website/src/namelist.txt', 'r') as file:
    names = file.read().splitlines()


def gen_frame(camera):
    global face_id, start_cam, varify
    while True:
        if start_cam:
            frame = camera.get_frames()
            yield (b'--frame\r\n'
                   b'Content-Type:  image/jpeg\r\n\r\n' + frame[0] +
                   b'\r\n\r\n')

            if frame[1] >= 0:
                face_id.append(frame[1])
                if len(face_id) == 10:
                    start_cam = False
                    for elm in face_id:
                        if face_id[0] != elm:
                            break

        else:
            break


@views.route('/video_feed')
def video_feed():
    return Response(gen_frame(Video()), mimetype='multipart/x-mixed-replace; boundary=frame', )


@views.route('/chatlog')
def chatlog():
    return render_template('home.html')


@views.route('/', methods=['POST', 'GET'])
def task():
    global start_cam, face_id, massages

    if request.method == 'POST':
        if request.form.get('stop') == 'Stop/Start':

            if not start_cam:
                start_cam = True
                face_id = []
            else:
                start_cam = False

        if request.form.get('Reset') == 'Reset':
            start_cam = True
            massages = []
            face_id = []

        if request.form.get('Take') == 'Take':
            massages.append(f"{names(face_id[0] - 1)} attendent have taken")
            start_cam = True
            face_id = []

    return render_template('home.html', massages=massages)
