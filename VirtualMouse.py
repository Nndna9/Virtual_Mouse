import cv2
import mediapipe as mp
import pyautogui

# Define your desired fixed resolution
fixed_width = 1920  # Replace with your desired width
fixed_height = 1080  # Replace with your desired height

# Set the screen resolution to the fixed values
pyautogui.FAILSAFE = False  # Disable failsafe (move to corner to stop)
pyautogui.PAUSE = 0.1  # Adjust the pause duration if needed

# Check if the current resolution matches the desired resolution
current_width, current_height = pyautogui.size()
if current_width != fixed_width or current_height != fixed_height:
    pyautogui.hotkey('win', 'p')  # Open Windows display settings (for Windows)
    pyautogui.typewrite(['down', 'enter', 'enter'])  # Select "PC screen only" and confirm
    pyautogui.sleep(2)  # Give time for the display settings to apply

# Now the screen resolution is set to the fixed values (1920x1080 in this example)

# Create an OpenCV window with fixed size
cv2.namedWindow('Virtual Mouse', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Virtual Mouse', fixed_width, fixed_height)

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print('outside', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    if abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
