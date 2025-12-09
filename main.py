from flask import Flask, Response
import cv2
import pygame
import os
import time

app = Flask(__name__)

BASE_PATH = r"G:\My Drive\drowsiness_project"

FACE_CASCADE_PATH = os.path.join(BASE_PATH, "haarcascade", "haarcascade_frontalface_default.xml")
EYE_CASCADE_PATH = os.path.join(BASE_PATH, "haarcascade", "haarcascade_eye.xml")
ALARM_PATH = os.path.join(BASE_PATH, "sound", "alarm.wav")

# Load cascades
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
eye_cascade = cv2.CascadeClassifier(EYE_CASCADE_PATH)

# Init sound
pygame.mixer.init()
pygame.mixer.music.load(ALARM_PATH)

# ✅ Safer camera fallback
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ CAMERA NOT FOUND")
    exit()
else:
    print("✅ CAMERA STARTED SUCCESSFULLY")

fatigue_score = 0
THRESHOLD = 8   # ✅ Lower threshold so alarm surely triggers
last_alarm_time = 0

def generate_frames():
    global fatigue_score, last_alarm_time

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        eyes_detected = False

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            roi_gray = gray[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4)

            if len(eyes) > 0:
                eyes_detected = True
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(frame,
                                  (x+ex, y+ey),
                                  (x+ex+ew, y+ey+eh),
                                  (255, 0, 0), 2)

        # ✅ FATIGUE LOGIC
        if len(faces) > 0 and not eyes_detected:
            fatigue_score += 2
        else:
            fatigue_score -= 1

        if fatigue_score < 0:
            fatigue_score = 0

        cv2.putText(frame, f"Fatigue Score: {fatigue_score}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # ✅ ALARM TRIGGER
        if fatigue_score >= 8:
            cv2.putText(frame, "DROWSINESS ALERT!", (80, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)

            if time.time() - last_alarm_time > 1.5:
                pygame.mixer.music.stop()
                pygame.mixer.music.play()
                last_alarm_time = time.time()

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Universal Driver Drowsiness Detection</title>
    </head>
    <body style="text-align:center; background:black; color:white;">
        <h1>Universal Drowsiness Detection System</h1>
        <img src="/video">
        <p>Detects Drowsiness for Any Person in Front of Camera</p>
    </body>
    </html>
    """

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run()
