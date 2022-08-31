from multiprocessing import Process, Manager

import cv2

from cam_pose import cam_pose
from tube_pose import tube_pose

TEST_URL = "https://www.youtube.com/shorts/FECEcjQ35EE"

if __name__ == '__main__':

    manager = Manager()
    shared_dict = manager.dict()  # 프로세스 간 공유되는 객체

    video = Process(target=tube_pose, args=(shared_dict, TEST_URL))
    video.start()

    if shared_dict.get("tube_output") is not None:
        cv2.imshow('camPose', shared_dict.get("video_output"))

    cam = Process(target=cam_pose, args=(shared_dict,))
    cam.start()

    if shared_dict.get("cam_output") is not None:
        cv2.imshow('camPose', shared_dict.get("cam_output"))

    video.join()
    cam.join()