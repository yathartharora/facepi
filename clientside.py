from imutils.video import VideoStream 
import imagezmq 
import argparse 
import socket 
import time 
import RPi.GPIO as GPIO

TCP_IP = '192.168.86.23'
TCP_PORT = 5999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen()
print("DONE.....")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)

ap = argparse.ArgumentParser()
ap.add_argument("-s","--server-ip",required=True,help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())

sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(args["server_ip"]))
print("Connected")

rpiName = socket.gethostname()
vs = VideoStream(usePiCamera=True,resolution=(640,480),framerate=32).start()
time.sleep(2.0)

while True:
    frame = vs.read()
    sender.send_image(rpiName,frame)
    s.listen()
    conn, addr = s.accept()
    data = conn.recv(20).decode()
    print(data)
    conn.send(data.encode())
    if data == "DETECTED":
        GPIO.output(23,GPIO.HIGH)
        time.sleep(5)
        GPIO.output(23,GPIO.LOW)
conn.close()



