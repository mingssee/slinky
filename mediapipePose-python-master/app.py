import argparse
import logging
import os
from multiprocessing import Process, Manager

import cv2
from flask import Flask, render_template, Response, request

from cam_pose import cam_pose
from tube_pose import tube_pose

logger = logging.getLogger("app")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')


# @app.route('/link')
# def link():
#     return render_template('link.html')


@app.route('/slinky', methods=['post'])
def slinky():
    video_feed_url = "/video_feed?video_url={request.args.to_dict().get('link')}"
    print(video_feed_url)

    return render_template('pose.html', video_feed_url=video_feed_url)


@app.route("/video_feed")
def video_feed():
    video_url = request.args.to_dict().get('video_url')

    tube = generate_video(video_url)

    return Response(tube,
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/cam_feed")
def cam_feed():
    cam = generate_cam()
    return Response(cam,
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def generate_cam():
    manager = Manager()
    shared_dict = manager.dict()  # 프로세스 간 공유되는 객체

    cam = Process(target=cam_pose, args=(shared_dict,))
    cam.start()

    while True:
        if shared_dict.get('cam_output') is None:
            continue

        (cam_flag, cam_encoded_image) = cv2.imencode(".jpg", shared_dict.get('cam_output'))

        if not cam_flag:
            continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(cam_encoded_image) + b'\r\n')


def generate_video(video_url):
    manager = Manager()
    shared_dict = manager.dict()  # 프로세스 간 공유되는 객체

    tube = Process(target=tube_pose, args=(shared_dict, video_url))
    tube.start()

    cam = Process(target=cam_pose, args=(shared_dict,))
    cam.start()

    while True:
        if shared_dict.get('tube_output') is None or shared_dict.get('cam_output') is None:
            continue

        # TODO: 2개의 이미지를 하나로 만들어서 내보낸 걸 추후에는 분리할 필요 있음.
        # youtube 영상에서 추출한 position을 cam에 띄우기 위해서 2개의 이미지를 하나로 합침.
        new_image = cv2.hconcat([shared_dict.get('tube_output'), shared_dict.get('cam_output')])

        (new_flag, new_encoded_image) = cv2.imencode(".jpg", new_image)

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(new_encoded_image) + b'\r\n')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)