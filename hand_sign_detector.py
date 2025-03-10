import cv2
import mediapipe as mp
import numpy as np
import time
import threading
import pyttsx3
from math import sqrt

# Initialize MediaPipe Hands and Drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize webcam feed
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Utility function to calculate Euclidean distance
def distance(point1, point2):
    return sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

# Function to handle speaking gestures
def speak_gesture(gesture):
    text_to_speak = {
        "Hello": "Hello",
        "fine": "Fine",
        "Not good": "Not good",
        "cool": "Cool",
        "Help": "Please help",
        "Thank you": "Thank You"
    }.get(gesture, "")

    if text_to_speak:
        try:
            engine.say(text_to_speak)
            engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

# Function to detect single-hand gestures
def detect_single_hand_gesture(hand):
    landmarks = hand['landmarks']

    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # Calculate thumb-index distance for gesture checks
    thumb_index_distance = distance(thumb_tip, index_finger_tip)

    # Confidence threshold
    confidence_scores = {
        "Hello": thumb_index_distance > 0.1,
        "fine": thumb_tip.y < index_finger_tip.y,
        "Not good": thumb_tip.y > index_finger_tip.y,
        "cool": thumb_index_distance > 0.15,
        "Help": thumb_tip.x < index_finger_tip.x
    }

    best_gesture = max(confidence_scores, key=confidence_scores.get)
    best_confidence = confidence_scores[best_gesture]

    return (best_gesture, 1.0) if best_confidence else (None, 0.0)

# Gesture recognition function
def detect_gesture(hands_data):
    if len(hands_data) == 1:
        return detect_single_hand_gesture(hands_data[0])
    return None, 0.0

# Start MediaPipe Hands
with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8
) as hands:
    last_gesture = None
    last_time = time.time()
    delay = 1.0
    gesture_history = []
    gesture_confidence_threshold = 7  # Improved threshold for stability

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: No frame captured.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        hands_data = []
        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                hand_info = {
                    'landmarks': hand_landmarks.landmark,
                    'handedness': handedness.classification[0].label
                }
                hands_data.append(hand_info)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        gesture, confidence = detect_gesture(hands_data)

        current_time = time.time()
        if gesture and confidence >= 0.8:
            gesture_history.append(gesture)
            if len(gesture_history) > 10:
                gesture_history.pop(0)

            if gesture_history.count(gesture) >= gesture_confidence_threshold:
                if gesture != last_gesture or (current_time - last_time) > delay:
                    last_gesture = gesture
                    last_time = current_time
                    threading.Thread(target=speak_gesture, args=(last_gesture,), daemon=True).start()

        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)  # Moved conversion before displaying text
        if last_gesture:
            cv2.putText(frame, f"{last_gesture} (Confidence: {confidence:.2f})",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

