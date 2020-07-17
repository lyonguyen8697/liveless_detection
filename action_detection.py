import cv2
import numpy as np


def draw_text_center(image, text, position):
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 2, 2)
    text_x = int(position[0] - int(text_size[0] / 2))
    text_y = position[1]
    cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)


def calculate_area(contours):
    return cv2.contourArea(np.array(contours))


def calculate_face_center(face):
    x = (face['chin'][0][0] + face['chin'][-1][0]) / 2
    y = (face['chin'][0][1] + face['chin'][-1][1]) / 2
    return np.array([x, y])


def find_nearest_face(face_landmarks, center):
    min_distance = 99999
    index = None
    for i, face in enumerate(face_landmarks):
        face_center = calculate_face_center(face)
        distance = np.linalg.norm(face_center - center)
        # print(distance)
        if distance < min_distance:
            min_distance = distance
            index = i

    return index


def is_face_in_ellipse():
    pass


def is_face_fit_ellipse(face, center, ellipse_axes):
    face_center = calculate_face_center(face)
    distance_to_center = np.linalg.norm(face_center - center)
    if distance_to_center > 30.0:
        return False, 'Fit your head in the ellipse'
    face_area = cv2.contourArea(face['chin'])
    ellipse_area = np.pi * ellipse_axes[0] * ellipse_axes[1]
    ratio = face_area / ellipse_area
    if 0.25 < ratio < 0.7:
        return True, 'Good job'
    return False, 'Fit your head in the ellipse'


def turn_your_head_up(face, center, ellipse_axes):
    face_center = calculate_face_center(face)
    nose_tip = face['nose_bridge'][-1]
    x_diff = abs(face_center[0] - nose_tip[0])
    y_diff= face_center[1] - nose_tip[1]
    if x_diff < 20.0 and y_diff > 0.0:
        return True, 'Great'
    return False, 'Turn your head up'


def turn_your_head_down(face, center, ellipse_axes):
    face_center = calculate_face_center(face)
    nose_bridge = face['nose_bridge'][0]
    x_diff = abs(face_center[0] - nose_bridge[0])
    y_diff = nose_bridge[1] - face_center[1]
    if x_diff < 20.0 and y_diff > 5.0:
        return True, 'Exactly'
    return False, 'Turn your head down'


def turn_your_head_left(face, center, ellipse_axes):
    face_center = calculate_face_center(face)
    nose_tip = face['nose_bridge'][-1]
    if nose_tip[0] - face_center[0] > 40.0:
        return True, 'You\' doing great'
    return False, 'Turn your head left'


def turn_your_head_right(face, center, ellipse_axes):
    face_center = calculate_face_center(face)
    nose_tip = face['nose_bridge'][-1]
    if face_center[0] - nose_tip[0]> 40.0:
        return True, 'You\' doing great'
    return False, 'Turn your head right'


def open_your_mouth(face, center, ellipse_axes):
    top_lip = face['top_lip'][-3]
    bottom_lip = face['bottom_lip'][-3]
    if bottom_lip[1] - top_lip[1] > 25.0:
        return True, 'Very good'
    return False, 'Open your mouth'


def close_your_left_eye(face, center, ellipse_axes):
    # Swap eye because the frame are flipped
    left_eye = face['right_eye']
    eye_aspect_ratio = (np.linalg.norm(left_eye[1] - left_eye[5]) + np.linalg.norm(left_eye[2] - left_eye[4])) \
                       / 2 * (np.linalg.norm(left_eye[0] - left_eye[3]))
    if eye_aspect_ratio < 200.0:
        return True, 'Good'
    return False, 'Close your left eye'


def close_your_right_eye(face, center, ellipse_axes):
    # Swap eye because the frame are flipped
    right_eye = face['left_eye']
    eye_aspect_ratio = (np.linalg.norm(right_eye[1] - right_eye[5]) + np.linalg.norm(right_eye[2] - right_eye[4])) \
                       / 2 * (np.linalg.norm(right_eye[0] - right_eye[3]))
    if eye_aspect_ratio < 200.0:
        return True, 'Good'
    return False, 'Close your right eye'

def verify_chain(actions, stage, face, center, ellipse_axes):
    action = actions[stage]

    result, status = action(face, center, ellipse_axes)

    result



