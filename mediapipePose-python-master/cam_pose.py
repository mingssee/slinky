import logging
import sys
import time

import cv2

from PoseModule import PoseDetector

logger = logging.getLogger("cam_pose")
logging.basicConfig(level=logging.DEBUG)

sys.path.append("tube_pose.py")


def cam_pose(shared_dict):
    cap = cv2.VideoCapture(0)
    p_time = 0
    detector = PoseDetector()

    while True:
        # if not shared_dict:
        #     continue

        success, img2 = cap.read()
        img2 = cv2.flip(img2, 1)
        img2 = cv2.resize(img2, (640, 400))
        # 사용자가 보기 편하게 좌우 반전
        img2 = detector.findPose(img2)
        lm_list2 = detector.findPosition(img2, draw=False)
        # if len(lm_list2) != 0:
        #     # print(lm_list2[14])
        #     cv2.circle(img2, (lm_list2[14][1], lm_list2[14][2]), 15, (0, 0, 255), cv2.FILLED)

        # logger.debug(shared_dict)

        try:
            _add_body_lines(img2, shared_dict)
        except:
            print("동영상이 아직 로드되지 않았습니다.")

        cTime = time.time()
        fps = 1 / (cTime - p_time)
        p_time = cTime

        # cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
        # (255, 0, 0), 3)
        # cv2.imshow('camPose', img2)
        shared_dict['cam_output'] = img2.copy()

        if cv2.waitKey(1) == ord('q'):
            break


def _add_body_lines(image, body_positions: dict):
    for i in range(11, 15):  # 양팔 추가
        if body_positions[i] is not None and body_positions[i + 2] is not None:
            cv2.line(image, body_positions[i], body_positions[i + 2], (255, 255, 255), 3)

    for i in [11]:  # 어깨 추가
        if body_positions[i] is not None and body_positions[i + 1] is not None:
            cv2.line(image, body_positions[i], body_positions[i + 1], (255, 255, 255), 3)

    for i in [23]:  # 배 추가
        if body_positions[i] is not None and body_positions[i + 1] is not None:
            cv2.line(image, body_positions[i], body_positions[i + 1], (255, 255, 255), 3)

    for i in [11, 12]:  # 어깨와 배 연결하여, 네모 모양 만듦
        if body_positions[i] is not None and body_positions[i + 12] is not None:
            cv2.line(image, body_positions[i], body_positions[i + 12], (255, 255, 255), 3)

    for i in [23, 24]:  # 다리 추가
        if body_positions[i] is not None and body_positions[i + 2] is not None and body_positions[i + 4] is not None:
            cv2.line(image, body_positions[i], body_positions[i + 2], (255, 255, 255), 3)
            cv2.line(image, body_positions[i + 2], body_positions[i + 4], (255, 255, 255), 3)