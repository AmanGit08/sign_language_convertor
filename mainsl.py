import cv2
import mediapipe as mp
import pyttsx3
import time

def classify_letter(landmarks):
    # Function to check if a finger is extended
    def is_finger_extended(tip, pip, mcp):
        return tip.y < pip.y < mcp.y

    thumb_extended = is_finger_extended(landmarks[4], landmarks[3], landmarks[2])
    index_extended = is_finger_extended(landmarks[8], landmarks[6], landmarks[5])
    middle_extended = is_finger_extended(landmarks[12], landmarks[10], landmarks[9])
    ring_extended = is_finger_extended(landmarks[16], landmarks[14], landmarks[13])
    pinky_extended = is_finger_extended(landmarks[20], landmarks[18], landmarks[17])

    extended = []
    if thumb_extended:
        extended.append('thumb')
    if index_extended:
        extended.append('index')
    if middle_extended:
        extended.append('middle')
    if ring_extended:
        extended.append('ring')
    if pinky_extended:
        extended.append('pinky')
    extended_set = set(extended)

    if extended_set == {'thumb'}:
        if landmarks[4].x > landmarks[3].x:  # thumb to the side for A
            return 'A'
        else:
            return 'T'  # thumb up for T
    elif extended_set == {'index', 'middle', 'ring', 'pinky'}:
        return 'B'
    elif extended_set == {'index', 'middle', 'ring'}:
        return 'W'
    elif extended_set == {'index', 'middle'}:
        if abs(landmarks[8].x - landmarks[12].x) < 0.05:
            return 'U'
        elif abs(landmarks[8].x - landmarks[12].x) > 0.1:
            return 'V'
        else:
            if landmarks[8].x > landmarks[12].x:
                return 'H'
            else:
                return 'V'
    elif extended_set == {'index'}:
        return 'D'
    elif extended_set == set():
        if abs(landmarks[4].x - landmarks[20].x) < 0.1 and abs(landmarks[4].y - landmarks[20].y) < 0.1:
            return 'O'
        elif abs(landmarks[4].x - landmarks[8].x) < 0.05 and abs(landmarks[4].y - landmarks[8].y) < 0.05:
            return 'F'
        elif landmarks[4].y < landmarks[9].y:
            return 'S'
        else:
            return 'E'
    elif extended_set == {'index', 'thumb'}:
        if landmarks[4].y > landmarks[8].y:
            return 'L'
        else:
            return 'G'
    elif extended_set == {'index', 'middle', 'thumb'}:
        return 'K'
    elif extended_set == {'thumb', 'index', 'middle'}:
        return 'M'
    elif extended_set == {'thumb', 'index', 'middle', 'ring'}:
        return 'N'
    elif extended_set == {'pinky'}:
        return 'I'
    elif extended_set == {'thumb', 'pinky'}:
        if landmarks[4].x < landmarks[20].x:
            return 'P'
        else:
            return 'Q'
    elif not index_extended and thumb_extended and middle_extended and ring_extended and pinky_extended:
        return 'X'
    elif extended_set == {'thumb', 'index', 'middle', 'ring', 'pinky'}:
        return 'B'  # all extended
    return ''

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize text-to-speech
engine = pyttsx3.init()

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

word = ""
last_letter = ""
last_time = time.time()
no_hand_time = 2  # seconds to wait before speaking word

print("Starting Sign Language Recognition. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    results = hands.process(rgb_frame)

    current_letter = ""
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark
            current_letter = classify_letter(landmarks)
            if current_letter and current_letter != last_letter:
                word += current_letter
                last_letter = current_letter
                last_time = time.time()
                print(f"Added letter: {current_letter}, Word: {word}")
    else:
        if time.time() - last_time > no_hand_time and word:
            print(f"Speaking word: {word}")
            engine.say(word)
            engine.runAndWait()
            word = ""
            last_letter = ""

    # Display current word
    cv2.putText(frame, f"Word: {word}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Last letter: {last_letter}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Sign Language Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
