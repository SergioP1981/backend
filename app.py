# app.py
import subprocess
import uuid
from flask import Flask, request, jsonify, send_file
import requests
from werkzeug.utils import secure_filename
import os
import ffmpeg


def create_app():
    app = Flask(__name__, static_folder='uploads', static_url_path='/uploads')
    app.config['UPLOAD_FOLDER'] = '/app/uploads/'
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Other setup code...
    return app


app = create_app()


@app.route('/', methods=['GET'])
def homepage():
    return "Homepage"


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

import requests
import cv2
import json

from flask import Flask, request

app = Flask(__name__)

@app.route('/video_length', methods=['POST'])
def video_length():
    data = request.get_json()
    video_url = data.get('video_url')

    # Download the video file
    response = requests.get(video_url, stream=True)
    response.raise_for_status()

    # Save the video file temporarily
    video_filename = '/tmp/video.mp4'  # Adjust the path as per your requirements
    with open(video_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Open the video file using OpenCV
    video = cv2.VideoCapture(video_filename)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    video_length = total_frames / fps

    # Clean up the temporary video file
    video.release()
    cv2.destroyAllWindows()
    if os.path.exists(video_filename):
        os.remove(video_filename)

    response_data = {
        'video_length': video_length
    }
    return json.dumps(response_data)

if __name__ == '__main__':
    app.run()

