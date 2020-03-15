# Tem plik to tylko przykład, trzeba to opakować w klasę z interfejsem(interfejsów nie ma w pythonie)
import cv2
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

# Część nagrywanka do opakowania w osobną metodę/część procesora
vrec = cv2.VideoWriter(
    'XD.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 30, (1920, 1080))  # dedukcja

# Ten sam config odbiera stream z kamerki i ffmpeg
vcap = cv2.VideoCapture("udp://0.0.0.0:8444", cv2.CAP_FFMPEG)
while(1):
    ret, frame = vcap.read()
    if frame is not None:
        vrec.write(frame)
        cv2.imshow('VIDEO', frame)
    c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):
        break


# Cleanup, tez musi być tam metoda jakaś taka
vrec.release()
vcap.release()
cv2.destroyAllWindows()
