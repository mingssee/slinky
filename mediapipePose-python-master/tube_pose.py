import logging

import cv2
import pafy
from cv2 import CAP_PROP_FPS

from PoseModule import PoseDetector

logger = logging.getLogger("tube_pose")
logging.basicConfig(level=logging.DEBUG)

lmList1 = []
x = []
y = []


def tube_pose(shared_dict: dict, link):
    # url = "https://www.youtube.com/watch?v=1W9gMxLoW6Q"
    url = link
    video = pafy.new(url)

    best = video.getbest(preftype="mp4")
    print("best resolution : {}".format(best.resolution))

    cap = cv2.VideoCapture(best.url)

    detector = PoseDetector()
    videofps = cap.get(CAP_PROP_FPS)
    print("fps -> ", videofps)
    delay = round(1000 / videofps)

    while True:
        success, img1 = cap.read()
        if not success:
            print('가져올 프레임 없음')
            break

        img1 = cv2.resize(img1, (640, 400))

        img1 = detector.findPose(img1)
        lm_list1 = detector.findPosition(img1, draw=False)
        # print(lm_list1)

        for item in lm_list1:
            shared_dict[item[0]] = (item[1], item[2])
        # logger.debug(shared_dict)
        # pos_list.append(lm_string)
        #
        # print("tube_pose : ", lm_string)

        # cTime = time.time()
        # fps = videofps
        # pTime = cTime

        # cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
        # (255, 0, 0), 5)

        # cv2.imshow('videoPose', img1)
        shared_dict['tube_output'] = img1.copy()
        if (cv2.waitKey(delay) == 27) | (cv2.waitKey(1) == ord('q')):
            break
        # if key == ord('s'):
        # with open("/Users/ming/PycharmProjects/pythonProject/2Dposition.txt", 'w') as f:
        #    f.writelines(["%s\n" % item for item in posList])