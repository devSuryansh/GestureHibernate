import cv2
import mediapipe as mp
import os
import platform
import time

# ----- CONFIG -----
ENABLE_HIBERNATE = True
HIBERNATE_DELAY = 0
# ------------------

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

def is_middle_finger_facing_camera(landmarks):
    """
    Detect if the middle finger is raised toward the camera and all other fingers are folded.
    """
    wrist = landmarks[0]
    middle_tip, middle_pip, middle_mcp = landmarks[12], landmarks[10], landmarks[9]
    thumb_tip, thumb_ip = landmarks[4], landmarks[3]
    index_tip, index_pip = landmarks[8], landmarks[6]
    ring_tip, ring_pip = landmarks[16], landmarks[14]
    pinky_tip, pinky_pip = landmarks[20], landmarks[18]

    is_palm_facing = wrist.z > middle_mcp.z
    is_middle_up = middle_tip.y < middle_pip.y
    are_others_down = (
        thumb_tip.y > thumb_ip.y and
        index_tip.y > index_pip.y and
        ring_tip.y > ring_pip.y and
        pinky_tip.y > pinky_pip.y
    )

    return is_palm_facing and is_middle_up and are_others_down

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

            if is_middle_finger_facing_camera(hand_landmarks.landmark):
                cv2.putText(frame, "Middle Finger Gesture Detected", (30, 50),
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

    cv2.imshow('Gesture Detection', frame)
    if cv2.waitKey(5) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
