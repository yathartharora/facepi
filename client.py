from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time
import RPi.GPIO as GPIO
import os

TCP_IP = '192.168.86.49'
TCP_PORT = 5999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen()
print("DONE.....")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

#ap = argparse.ArgumentParser()
#ap.add_argument("-s","--server-ip",required=True,help="ip address of the server to which the client will connect")
#args = vars(ap.parse_args())

sender = imagezmq.ImageSender(connect_to="tcp://192.168.86.69:4900")
print("Connected")

rpiName = socket.gethostname()
vs = VideoStream(usePiCamera=True,resolution=(640,480),framerate=40).start()
time.sleep(2.0)
GPIO.output(23,GPIO.HIGH)

while True:
    frame = vs.read()
    sender.send_image(rpiName,frame)
    s.listen()
    conn, addr = s.accept()
    data = conn.recv(1024).decode()
    print(data)
    conn.send(data.encode())
    if data == "DETECTED":
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(25,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(25,GPIO.LOW)
    if data == "EXIT":
        GPIO.output(23,GPIO.LOW)
        break
    GPIO.output(23,GPIO.HIGH)

os.system('sudo shutdown now -h')

