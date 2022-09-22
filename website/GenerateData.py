# from flask import Blueprint, render_template, Response, request
# from website.src.GenerateDataset import Capture
# from website.src.ProcessImages import process_photo
# from website.src.Train import train_photo
#
#
# GenerateData = Blueprint('GenerateData', __name__)
#
#
# @GenerateData.route('/GenerateData', methods=['POST', 'GET'])
# def generate():
#     if request.method == 'POST':
#         if request.form.get('Start') == 'Stop/Start':
#             Capture().capture_photo()
#
#         if request.form.get('process') == 'process':
#             process_photo()
#
#         if request.form.get('Train') == 'Train':
#             train_photo()
#
#     return render_template('generateData.html')