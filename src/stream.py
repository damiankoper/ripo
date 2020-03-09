import cv2
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
vrec = cv2.VideoWriter(
    'XD.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 30, (1920, 1080))
vcap = cv2.VideoCapture("udp://0.0.0.0:8444", cv2.CAP_FFMPEG)
while(1):
    ret, frame = vcap.read()
    vrec.write(frame)
    cv2.imshow('VIDEO', frame)
    c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):
        break
vrec.release()
vcap.release()
cv2.destroyAllWindows()
