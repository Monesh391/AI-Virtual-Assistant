import cv2
import mediapipe as mp
import time
import math


class HandDetector:

    def __init__(
        self,
        mode=False,
        maxHands=1,
        modelComplexity=1,
        detectionCon=0.8,
        trackCon=0.8,
    ):

        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            model_complexity=self.modelComplexity,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon,
        )

        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

        self.lmList = []

        self.results = None

        self.handType = "Right"
            # ----------------------------
    # FIND HANDS
    # ----------------------------

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:

            if self.results.multi_handedness:
                self.handType = (
                    self.results.multi_handedness[0]
                    .classification[0]
                    .label
                )

            for handLms in self.results.multi_hand_landmarks:

                if draw:

                    self.mpDraw.draw_landmarks(
                        img,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS
                    )

        return img
        # ----------------------------
    # FIND HAND LANDMARK POSITIONS
    # ----------------------------

    def findpostion(
        self,
        img,
        handNo=0,
        draw=True,
        blue=255,
        green=255,
        red=255,
    ):

        self.lmList = []

        xList = []
        yList = []
        bbox = []

        if self.results and self.results.multi_hand_landmarks:

            if handNo >= len(self.results.multi_hand_landmarks):
                return [], []

            myHand = self.results.multi_hand_landmarks[handNo]

            h, w, c = img.shape

            for id, lm in enumerate(myHand.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                xList.append(cx)
                yList.append(cy)

                self.lmList.append([id, cx, cy])

                if draw:

                    cv2.circle(
                        img,
                        (cx, cy),
                        5,
                        (blue, green, red),
                        cv2.FILLED
                    )

            xmin = min(xList)
            xmax = max(xList)
            ymin = min(yList)
            ymax = max(yList)

            bbox = (xmin, ymin, xmax, ymax)

            if draw:

                cv2.rectangle(
                    img,
                    (xmin - 20, ymin - 20),
                    (xmax + 20, ymax + 20),
                    (0, 255, 0),
                    2
                )

        return self.lmList, bbox
        # ----------------------------
    # CHECK WHICH FINGERS ARE UP
    # ----------------------------

    def fingersUp(self):

        fingers = []

        if len(self.lmList) == 0:
            return [0, 0, 0, 0, 0]

        # Detect Left / Right Hand
        if self.handType == "Right":

            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        else:

            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Index, Middle, Ring, Pinky

        for i in range(1, 5):

            if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
        # ----------------------------
    # FIND DISTANCE BETWEEN TWO LANDMARKS
    # ----------------------------

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):

        if len(self.lmList) == 0:
            return 0, img, []

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if draw:

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)

            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


# ----------------------------
# FPS CLASS
# ----------------------------

class FPS:

    def __init__(self):

        self.pTime = 0

    def get_fps(self, img, blue=255, green=255, red=255):

        cTime = time.time()

        fps = 0

        if cTime != self.pTime:
            fps = 1 / (cTime - self.pTime)

        self.pTime = cTime

        cv2.putText(
            img,
            f"FPS: {int(fps)}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (blue, green, red),
            2,
        )