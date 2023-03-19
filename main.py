import cv2
import time
import streamlit as st
from timer import get_time, get_day

st.title("Motion Detector")
start = st.button("Start Camera")

if start:
    streamlit_image = st.image([])
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    first_frame = None
    # Status - motion detector.
    status_list = [0, 0]

    while True:
        # Status - motion detector.
        status = 0
        check, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
        # cv2.imshow("My video", gray_frame_gau)

        # Set the first frame.
        if first_frame is None:
            first_frame = gray_frame_gau

        delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
        # cv2.imshow("My video", delta_frame)

        thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
        # cv2.imshow("My video", dil_frame)

        contours, check = cv2.findContours(dil_frame,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

        # Add the rectangle.
        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            else:
                x, y, w, h = cv2.boundingRect(contour)
                rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                if rectangle.any():
                    # Status - motion detector.
                    status = 1

        # Send en email when motion is detected and status_list is [1, 0] - end of movement
        status_list[0] = status_list[1]
        status_list[1] = status
        if status_list[0] == 1 and status_list[1] == 0:
            print("Sending message")

        # Add day of the week and date to the frame.
        cv2.putText(img=frame, text=get_day(), org=(50, 50),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img=frame, text=get_time(), org=(50, 90),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(200, 100, 20),
                    thickness=2, lineType=cv2.LINE_AA)

        # cv2.imshow("My video", frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        streamlit_image.image(frame)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    cap.release()
