import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import pyautogui
import time

pyautogui.FAILSAFE = False

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
face_options = vision.FaceLandmarkerOptions(base_options = python.BaseOptions(model_asset_path = 'face_landmarker.task'), output_face_blendshapes = True, num_faces = 1)

detector = vision.HandLandmarker.create_from_options(options)
face_detector = vision.FaceLandmarker.create_from_options(face_options)

SCREEN_W, SCREEN_H = pyautogui.size()
pointer_enabled = False
bx, by, bw, bh = 0, 0, 160, 45
smooth_x, smooth_y = 0, 0
smoothing_factor = 5
last_click_time = 0
click_cooldown = 2.0

def mouse_callback(event, x, y, flags, param):
    global pointer_enabled
    if event == cv2.EVENT_LBUTTONDOWN:
        if bx <= x <= bx + bw and by <= y <= bh + by:
            pointer_enabled = not pointer_enabled

CONNECTIONS = [
    (1, 2), (2, 3), (3, 4),    
    (5, 6), (6, 7), (7, 8),    
    (9, 10), (10, 11), (11, 12), 
    (13, 14), (14, 15), (15, 16), 
    (17, 18), (18, 19), (19, 20)  
]
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
L_IRIS = 468
R_IRIS = 473

cap = cv2.VideoCapture(0)
rotation_angle = 0

cv2.namedWindow("AR Hand Skeleton")
cv2.setMouseCallback("AR Hand Skeleton", mouse_callback)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    face_result = face_detector.detect(mp_image)
    result = detector.detect(mp_image)

    bx, by = w - 180, h - 70

    if face_result.face_landmarks:
        for face_landmarks in face_result.face_landmarks:
            for eye_indices in [LEFT_EYE, RIGHT_EYE]:
                eye_coords = [(int(face_landmarks[i].x*w), int(face_landmarks[i].y*h)) for i in eye_indices]
                x_coords = [p[0] for p in eye_coords]
                y_coords = [p[1] for p in eye_coords]
                margin = 10
                min_x, max_x = min(x_coords) - margin, max(x_coords) + margin
                min_y, max_y = min(y_coords) - margin, max(y_coords) + margin
                cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 1)
                cv2.line(frame, (min_x, min_y), (min_x + 5, min_y), (255, 255, 255), 2)
                cv2.line(frame, (min_x, min_y), (min_x, min_y + 5), (255, 255, 255), 2)
            for idx in [L_IRIS, R_IRIS]:
                cx = int(face_landmarks[idx].x*w)
                cy = int(face_landmarks[idx].y*h)
                cv2.circle(frame, (cx, cy), 1, (0, 0, 255), -1)
                cv2.circle(frame, (cx, cy), 8, (0, 0, 255), 1)
                cv2.line(frame, (cx - 12, cy), (cx + 12, cy), (0, 0, 255), 1)
                cv2.line(frame, (cx, cy - 12), (cx, cy + 12), (0, 0, 255), 1)

    if result.hand_landmarks:
        primary_hand = result.hand_landmarks[0]
        idx_tip = primary_hand[8]
        
        if pointer_enabled:
            m_pad = 0.2
            tx = np.interp(idx_tip.x, [m_pad, 1.0 - m_pad], [0, SCREEN_W])
            ty = np.interp(idx_tip.y, [m_pad, 1.0 - m_pad], [0, SCREEN_H])
            smooth_x += (tx - smooth_x)/smoothing_factor
            smooth_y += (ty - smooth_y)/smoothing_factor
            pyautogui.moveTo(int(smooth_x), int(smooth_y))

        for hand in result.hand_landmarks:
            coords = [(int(lm.x*w), int(lm.y*h)) for lm in hand]
            palm_center = (int((coords[0][0] + coords[5][0] + coords[17][0])/3), int((coords[0][1] + coords[5][1] + coords[17][1])/3))
            rotation_angle += 5
            cv2.ellipse(frame, palm_center, (35, 35), 0, rotation_angle, rotation_angle + 60, (255, 255, 255), 2)
            cv2.ellipse(frame, palm_center, (35, 35), 0, rotation_angle + 180, rotation_angle + 240, (255, 255, 255), 2)
            cv2.circle(frame, palm_center, 12, (255, 255, 255), -1)
            cv2.circle(frame, palm_center, 18, (255, 0, 150), 2)
            for b_idx in [2, 5, 9, 13, 17]:
                cv2.line(frame, palm_center, coords[b_idx], (255, 0, 150), 3)
                cv2.line(frame, palm_center, coords[b_idx], (255, 255, 255), 1)
            for s_idx, e_idx in CONNECTIONS:
                if (s_idx, e_idx) == (1, 2): continue
                cv2.line(frame, coords[s_idx], coords[e_idx], (255, 0, 150), 3)
                cv2.line(frame, coords[s_idx], coords[e_idx], (255, 255, 255), 1)
            for i in [4, 8, 12, 16, 20]:
                radius = int(abs(hand[i].z)*100) + 8
                cv2.circle(frame, coords[i], radius, (255, 0, 255), -1)
                cv2.circle(frame, coords[i], 3, (255, 255, 255), -1)

            if pointer_enabled:
                dist = np.linalg.norm(np.array(coords[4]) - np.array(coords[8]))
                current_time = time.time()
                if dist < 30 and (current_time - last_click_time) > click_cooldown:
                    pyautogui.click()
                    last_click_time = current_time
                    cv2.putText(frame, "CLICKED", (coords[8][0], coords[8][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    btn_color = (0, 255, 0) if pointer_enabled else (0, 0, 255)
    cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (255, 255, 255), -1)
    cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), btn_color, 2)
    label = "MOUSE: ON" if pointer_enabled else "MOUSE: OFF"
    cv2.putText(frame, label, (bx + 12, by + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, btn_color, 2)

    key = cv2.waitKey(1)
    if key & 0xFF == 27: break
    elif key & 0xFF == ord('m'):
        pointer_enabled = not pointer_enabled

    cv2.imshow("AR Hand Skeleton", frame)

detector.close()
cap.release()
cv2.destroyAllWindows()