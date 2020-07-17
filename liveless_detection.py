import face_recognition
import cv2
import numpy as np
import os

from action_detection import *

video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_landmarks = []
process_this_frame = True

status = 'Fit your face in the ellipse'
delay = 0
ellipse_axes = (100, 150)
ellipse_area = np.pi * (ellipse_axes[0] / 2) * (ellipse_axes[1] / 2)
actions = [
    turn_your_head_up,
    turn_your_head_down,
    turn_your_head_left,
    turn_your_head_right,
    open_your_mouth,
    close_your_left_eye,
    close_your_right_eye
]
stage = 0
finish = False

np.random.shuffle(actions)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_landmarks = face_recognition.face_landmarks(rgb_small_frame, face_locations)

        # Resize frame to original
        for face in face_landmarks:
            for key, points in face.items():
                face[key] = np.array(points) * 4

    process_this_frame = not process_this_frame

    ######################################
    # Verify face
    center = (int(frame.shape[1] / 2), int(frame.shape[0] / 2))

    face_id = find_nearest_face(face_landmarks, center)

    is_face_fit = False

    if face_id is not None and not finish:

        face = face_landmarks[face_id]

        is_face_fit, status_temp = is_face_fit_ellipse(face, center, ellipse_axes)

        if delay == 0:
            status = status_temp
            if is_face_fit:
                action = actions[stage]

                result, status = action(face, center, ellipse_axes)

                if result:
                    delay = 20
                    stage = stage + 1

                    if stage == len(actions):
                        status = 'Your face are verified'
                        finish = True
        else:
            if not is_face_fit:
                status = status_temp
            delay = delay - 1

    # Draw ellipse
    if is_face_fit or finish:
        frame = cv2.ellipse(frame, center, ellipse_axes, 0, 0, 360, (0, 255, 0), 3)
    else:
        frame = cv2.ellipse(frame, center, ellipse_axes, 0, 0, 360, (0, 0, 255), 3)

    # Flip frame
    frame = cv2.flip(frame, 1)

    draw_text_center(frame, status, (frame.shape[0] / 2, 50))

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
