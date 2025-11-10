import cv2

url = "rtsp://geocon:geocon1@192.168.1.131/stream1"
cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
if not cap.isOpened():
    print("❌ Failed to open stream")
else:
    print("✅ Stream opened")
    ret, frame = cap.read()
    print("Frame read:", ret, "Shape:" if frame is not None else None)
cap.release()
