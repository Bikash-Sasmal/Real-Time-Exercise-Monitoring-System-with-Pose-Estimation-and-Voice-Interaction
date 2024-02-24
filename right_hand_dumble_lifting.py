import cv2
import mediapipe as mp
import numpy as np
from calculate_angle import calculate_angle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.p

cap = cv2.VideoCapture(0)
counter = 0
stage = "up"

def perform_pose_right(hand = "right", side = "right"):
    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0
    stage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            result = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = result.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
             
                
                angle = calculate_angle(shoulder, elbow, wrist)
                cv2.putText(image, str(angle), tuple(np.multiply(elbow, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                

                if angle > 160:
                    stage = " down"
                    # speak("down")
                elif angle < 30 and stage == " down":
                    stage = " up"
                    counter += 1
                    print(counter)
                    # speak("up")
            except:
                pass

            cv2.rectangle(image, (0, 0), (255, 73), (245, 117, 16), -1)
            cv2.putText(image, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, 'STAGE', (65, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2), mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))

            cv2.imshow("Mediapipe Feed", image)

            if cv2.waitKey(10) & 0XFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()