from multiprocessing import Manager, Process

from flask import Flask, render_template, request

import logging

from cam_pose import cam_pose
from tube_pose import tube_pose

logger = logging.getLogger("app")

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/link')
def link():
    return render_template('link.html')

@app.route('/slinky', methods=['post'])
def slinky():
    link = request.form.get("link")
    print(link)

    manager = Manager()
    shared_dict = manager.dict()  # 프로세스 간 공유되는 객체

    video = Process(target=tube_pose, args=(shared_dict, link))
    video.start()

    cam = Process(target=cam_pose, args=(shared_dict,))
    cam.start()

    video.join()
    cam.join()

    # return render_template('pose.html', youtube_video=tube_pose(shared_dict=link), cam_video=cam)
    return render_template('pose.html')

if __name__=='__main__':
    app.run(debug=True)