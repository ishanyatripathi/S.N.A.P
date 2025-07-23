import cv2
import mediapipe as mp
import pyautogui
from collections import deque

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Variables to track gestures
snap_buffer_right = deque(maxlen=3)
snap_buffer_left = deque(maxlen=3)
SNAP_THRESHOLD = 15
COOLDOWN_FRAMES = 15
cooldown_counter = 0

def detect_snap(landmarks, frame_width, frame_height, snap_buffer):
    thumb_tip = landmarks[4]
    middle_tip = landmarks[12]
    thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
    middle_x, middle_y = int(middle_tip.x * frame_width), int(middle_tip.y * frame_height)

    distance = ((thumb_x - middle_x) ** 2 + (thumb_y - middle_y) ** 2) ** 0.5
    snap_buffer.append(distance)

    if len(snap_buffer) == snap_buffer.maxlen:
        start_distance = snap_buffer[0]
        end_distance = snap_buffer[-1]
        distance_change = start_distance - end_distance

        if distance_change > SNAP_THRESHOLD:
            return True

    return False

def is_hand_open(landmarks):
    return (
        landmarks[8].y < landmarks[6].y and     # Index finger
        landmarks[12].y < landmarks[10].y and   # Middle finger
        landmarks[16].y < landmarks[14].y and   # Ring finger
        landmarks[20].y < landmarks[18].y       # Pinky
    )

def detect_both_palms_open(hands_dict):
    return hands_dict.get("Left", False) and hands_dict.get("Right", False)

def process_frame(frame):
    global cooldown_counter

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    right_hand_snap = False
    left_hand_snap = False
    hands_open_status = {}

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            hand_label = handedness.classification[0].label

            # Snap gesture
            if hand_label == "Right":
                right_hand_snap = detect_snap(landmarks, frame.shape[1], frame.shape[0], snap_buffer_right)
            elif hand_label == "Left":
                left_hand_snap = detect_snap(landmarks, frame.shape[1], frame.shape[0], snap_buffer_left)

            # Hand open detection
            hands_open_status[hand_label] = is_hand_open(landmarks)

    # Exit presentation if both palms are open
    if detect_both_palms_open(hands_open_status) and cooldown_counter == 0:
        print("Gesture Detected: Both Palms Open (Close Presentation)")
        pyautogui.hotkey('alt', 'f4')
        cooldown_counter = COOLDOWN_FRAMES
    elif right_hand_snap and cooldown_counter == 0:
        print("Gesture Detected: Right Hand Snap (Next Slide)")
        pyautogui.press('right')
        cooldown_counter = COOLDOWN_FRAMES
    elif left_hand_snap and cooldown_counter == 0:
        print("Gesture Detected: Left Hand Snap (Previous Slide)")
        pyautogui.press('left')
        cooldown_counter = COOLDOWN_FRAMES

    if cooldown_counter > 0:
        cooldown_counter -= 1

    return frame

def main():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = process_frame(frame)
        cv2.imshow("Gesture-Controlled Presentation", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
