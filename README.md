# 🚗 Universal Driver Drowsiness Detection System  

A real-time AI-based driver drowsiness detection system built using **OpenCV, Flask, Haar Cascade, and Pygame** that monitors eye closure and triggers an alarm to prevent accidents caused by fatigue.

---

## 🔴 Live Project Website  
    https://harshitha-urss.github.io/driver-drowsiness-detection/

##  Project Demo Video  
    https://youtu.be/QTTx1YfluBc

---

## Problem Statement  
Driver fatigue is one of the leading causes of road accidents worldwide. Continuous real-time monitoring of driver alertness is essential to prevent loss of life. Manual monitoring is unreliable, hence an **automated driver drowsiness detection system** is required.

---

## System Features  
-  Real-time face detection  
-  Eye detection using Haar Cascade  
-  Fatigue score calculation  
-  Alarm alert on prolonged eye closure  
-  Flask-based live video streaming  
-  Lightweight and works on CPU  

---

## Technology Stack  
- **Programming Language:** Python  
- **Computer Vision:** OpenCV  
- **Web Framework:** Flask  
- **Detection Model:** Haar Cascade  
- **Audio Alert:** Pygame  
- **Frontend:** HTML, CSS  
- **Version Control:** Git & GitHub  

---

## System Architecture  
1. Webcam captures real-time frames  
2. Frames converted to grayscale  
3. Face detected using Haar Cascade  
4. Eye detection from face region  
5. Fatigue score calculated  
6. Alarm triggered if threshold exceeded  

---

## Results  
The system successfully detects eye closure in real time and triggers an alarm alert when fatigue is detected. It performs accurately under normal lighting conditions with minimal CPU usage.

---

## 📂 Project Structure
drowsiness_project/
│── data/
│── dataset/
│── haarcascade/
│── model/
│── sound/
│── main.py
│── train_model.py
│── capture_eyes.py
│── index.html
│── style.css
│── script.js


