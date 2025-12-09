import cv2
import os

BASE_PATH = r"G:\My Drive\drowsiness_project\dataset"
OPEN_PATH = os.path.join(BASE_PATH, "open")
CLOSED_PATH = os.path.join(BASE_PATH, "closed")

os.makedirs(OPEN_PATH, exist_ok=True)
os.makedirs(CLOSED_PATH, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

open_count = len(os.listdir(OPEN_PATH))
closed_count = len(os.listdir(CLOSED_PATH))

print("Press 'o' to save OPEN eye")
print("Press 'c' to save CLOSED eye")
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

        for (ex, ey, ew, eh) in eyes:
            eye_img = roi_gray[ey:ey+eh, ex:ex+ew]
            eye_img = cv2.resize(eye_img, (24, 24))

            cv2.imshow("Eye", eye_img)

            key = cv2.waitKey(1)

            if key == ord('o'):
                cv2.imwrite(os.path.join(OPEN_PATH, f"open_{open_count}.jpg"), eye_img)
                open_count += 1
                print("Saved OPEN eye:", open_count)

            elif key == ord('c'):
                cv2.imwrite(os.path.join(CLOSED_PATH, f"closed_{closed_count}.jpg"), eye_img)
                closed_count += 1
                print("Saved CLOSED eye:", closed_count)

    cv2.imshow("Capture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
