import cv2
import mediapipe as mp
import ssl
import time
import math

ssl._create_default_https_context = ssl._create_unverified_context


class PoseDetector:

    def __init__(self, mode=False, model_complexity=1, smooth_landmarks=True, enable_seg=False,
                 smooth_seg=True, detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_seg = enable_seg
        self.smooth_seg = smooth_seg
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.smooth_landmarks, self.enable_seg,
                                     self.smooth_seg, self.detectionCon, self.trackCon)
        #Pose의 def __init__(self,
             #static_image_mode: bool = False,
             #model_complexity: int = 1,
             #smooth_landmarks: bool = True,
             #enable_segmentation: bool = False,
             #smooth_segmentation: bool = True,
             #min_detection_confidence: float = 0.5,
             #min_tracking_confidence: float = 0.5) -> None


    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList=[]
        if self.results.pose_landmarks:
            #print(self.results.pose_landmarks)
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)  # flour, double x, pixel values o
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                    # cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)  # 오른팔꿈치만 크게 해본다면
        return self.lmList

    def findAngle(self, img, p1,p2,p3, draw=True):

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle=math.degrees(math.atan2(y3-y2,x3-x2)-
                           math.atan2(y1-y2,x1-x2))
        if angle<0:
            angle = -angle
        if 180<angle<360:
            angle = 360-angle

        #print(angle)


        if draw :
            cv2.line(img,(x1, y1),(x2, y2),(255,255,255),3)
            cv2.line(img,(x3, y3),(x2, y2),(255,255,255),3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img,str(int(angle)),(x2-50,y2+50),
                        cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        return angle

