import cv2
import mediapipe as mp
import os
import platform
import time
from collections import deque

# ----- CONFIG -----
ENABLE_HIBERNATE = False
HIBERNATE_DELAY = 0
WAVE_DETECTION_WINDOW = 10
WAVE_THRESHOLD = 3
MIN_MOVEMENT = 0.02  # Minimum movement to be considered a wave
# ------------------

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

def is_palm_open(landmarks):
    """
    Checks if all fingers are extended (open palm).
    """
    return (
        landmarks[4].y < landmarks[3].y and    # Thumb
        landmarks[8].y < landmarks[6].y and    # Index
        landmarks[12].y < landmarks[10].y and  # Middle
        landmarks[16].y < landmarks[14].y and  # Ring
        landmarks[20].y < landmarks[18].y      # Pinky
    )

def is_waving(x_history):
    if len(x_history) < 2:
        return False

    transitions = 0
    prev_direction = 0

    for i in range(1, len(x_history)):
        dx = x_history[i] - x_history[i - 1]
        if abs(dx) < MIN_MOVEMENT:
            continue  # Ignore tiny movement
        direction = 1 if dx > 0 else -1
        if direction != prev_direction and prev_direction != 0:
            transitions += 1
        prev_direction = direction

    return transitions >= WAVE_THRESHOLD

# Use hand center instead of just wrist for stability
def get_hand_center(landmarks):
    x_coords = [lm.x for lm in landmarks]
    return sum(x_coords) / len(x_coords)

hand_x_history = deque(maxlen=WAVE_DETECTION_WINDOW)
hibernate_triggered = False

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            center_x = get_hand_center(hand_landmarks.landmark)
            hand_x_history.append(center_x)

            if is_palm_open(hand_landmarks.landmark) and is_waving(list(hand_x_history)):
                cv2.putText(frame, "Waving Detected - Bye Bye!", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                if not hibernate_triggered:
                    hibernate_triggered = True
                    print(f"Hibernating in {HIBERNATE_DELAY} seconds...")
                    time.sleep(HIBERNATE_DELAY)

                    if ENABLE_HIBERNATE:
                        os_type = platform.system()
                        if os_type == 'Windows':
                            os.system("shutdown /h")
                        elif os_type in ['Linux', 'Darwin']:
                            os.system("systemctl hibernate")
                        else:
                            print("Unsupported OS for hibernation")
                    else:
                        print("[TEST MODE] Hibernate command triggered.")
                    break
            else:
                cv2.putText(frame, "Palm Detected - No Wave", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow('Waving Detection', frame)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
