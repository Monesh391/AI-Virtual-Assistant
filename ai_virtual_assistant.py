import cv2
import numpy as np
import pyautogui
import time
import threading

import HandTrakingModule as htm
from voice import speak
from voice_commands import process_voice_command

# ======================================
# CAMERA SETTINGS
# ======================================

wCam = 1280
hCam = 720

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam)
cap.set(cv2.CAP_PROP_FPS, 60)

# ======================================
# SCREEN SETTINGS
# ======================================

wScr, hScr = pyautogui.size()

print("Screen Resolution:", wScr, hScr)

# ======================================
# MOUSE SETTINGS
# ======================================

frameR = 40
smoothening = 1

plocX = 0
plocY = 0
clocX = 0
clocY = 0

voiceMode = False

# ======================================
# INITIALIZE HAND DETECTOR
# ======================================

detector = htm.HandDetector(
    maxHands=1,
    detectionCon=0.8,
    trackCon=0.8
)

fps = htm.FPS()

pyautogui.FAILSAFE = False

speak("AI Virtual Assistant Started")

# ======================================
# MAIN LOOP
# ======================================

while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    img = detector.findHands(img)

    lmList, bbox = detector.findpostion(
        img,
        draw=True,
        blue=0,
        green=0,
        red=255
    )

    # Control Area
    cv2.rectangle(
        img,
        (frameR, frameR),
        (wCam-frameR, hCam-frameR),
        (255, 0, 255),
        2
    )

    if len(lmList) != 0:

        fingers = detector.fingersUp()

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Display detected fingers
        cv2.putText(
            img,
            str(fingers),
            (20, 220),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        
                # ======================================
        # MOUSE MOVE
        # Gesture: Index Finger Only
        # ======================================

        if fingers == [0, 1, 0, 0, 0]:

            x3 = np.interp(
                x1,
                (frameR, wCam - frameR),
                (0, wScr)
            )

            y3 = np.interp(
                y1,
                (frameR, hCam - frameR),
                (0, hScr)
            )

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            pyautogui.moveTo(
                wScr - clocX,
                clocY
            )

            cv2.circle(
                img,
                (x1, y1),
                15,
                (255, 0, 255),
                cv2.FILLED
            )

            plocX = clocX
            plocY = clocY
                    # ======================================
        # LEFT CLICK
        # Gesture: Index + Middle
        # ======================================

        if fingers == [0, 1, 1, 0, 0]:

            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 35:

                pyautogui.click()

                cv2.circle(
                    img,
                    (lineInfo[4], lineInfo[5]),
                    15,
                    (0, 255, 0),
                    cv2.FILLED
                )

                speak("Left Click")

                time.sleep(0.3)

        # ======================================
        # RIGHT CLICK
        # Gesture: Index + Pinky
        # ======================================

        if fingers == [0, 1, 0, 0, 1]:

            length, img, lineInfo = detector.findDistance(8, 20, img)

            if length < 40:

                pyautogui.rightClick()

                cv2.circle(
                    img,
                    (lineInfo[4], lineInfo[5]),
                    15,
                    (255, 0, 0),
                    cv2.FILLED
                )

                speak("Right Click")

                time.sleep(0.3)

        # ======================================
        # DOUBLE CLICK
        # Gesture: Thumb + Index
        # ======================================

        if fingers == [1, 1, 0, 0, 0]:

            length, img, lineInfo = detector.findDistance(4, 8, img)

            if length < 35:

                pyautogui.doubleClick()

                speak("Double Click")

                time.sleep(0.4)

        # ======================================
        # DRAG & DROP
        # Gesture: Thumb + Index + Middle
        # ======================================

        if fingers == [1, 1, 1, 0, 0]:

            pyautogui.mouseDown()

            cv2.putText(
                img,
                "DRAGGING",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2
            )

        else:

            pyautogui.mouseUp()

        # ======================================
        # SCROLL UP
        # Gesture: Index + Middle + Ring
        # ======================================

        if fingers == [0, 1, 1, 1, 0]:

            pyautogui.scroll(250)

            cv2.putText(
                img,
                "SCROLL UP",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        # ======================================
        # SCROLL DOWN
        # Gesture: Index + Middle + Ring + Pinky
        # ======================================

        if fingers == [0, 1, 1, 1, 1]:

            pyautogui.scroll(-250)

            cv2.putText(
                img,
                "SCROLL DOWN",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )
                    # ======================================
        # VOICE COMMAND
        # Gesture: Thumb Only
        # ======================================

        if fingers == [1, 0, 0, 0, 0]:

            cv2.putText(
                img,
                "VOICE MODE",
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 0),
                2
            )

            if not voiceMode:

                voiceMode = True

                
                threading.Thread(
                     target=process_voice_command,
                     daemon=True
                     ).start()

                time.sleep(1)

        else:

            voiceMode = False
    # ======================================
    # SHOW FPS
    # ======================================

    fps.get_fps(
        img,
        blue=255,
        green=255,
        red=0
    )

    # ======================================
    # SHOW CAMERA WINDOW
    # ======================================

    cv2.imshow(
        "AI Virtual Assistant",
        img
    )

    # ======================================
    # EXIT
    # ======================================

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    # ======================================
# CLEANUP
# ======================================

cap.release()

cv2.destroyAllWindows()
