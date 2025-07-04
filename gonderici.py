import cv2
import mediapipe as mp
import socket
import time
#local soket gonderici
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]
        left_iris = landmarks.landmark[474]
        eye_x = left_iris.x
        eye_y = left_iris.y

        message = f"{eye_x:.4f},{eye_y:.4f}"
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        print(f"Gönderildi: {message}")

    time.sleep(0.02)