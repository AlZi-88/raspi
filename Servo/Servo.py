from time import *
from RPi import GPIO
from ADCDevice import *
from math import *

pwmPin = 12
fBas = 50
angMin = 0
angMax = 180
tMin = 0.5/1000
tMax = 2.5/1000
factor = (tMax - tMin)/(angMax - angMin)
offset = tMin - factor*angMin
print(factor, offset)

def setup():
    global f
    print(factor)
    print(offset)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pwmPin, GPIO.OUT)
    
    f = GPIO.PWM(pwmPin, fBas)
    f.start(0)
    f.ChangeDutyCycle(getDucy(0))

def getDucy(angReq):
    tReq = angReq*factor + offset
    print(int(100*tReq*fBas+1))
    return int(100*tReq*fBas+1)
    
def loop():
    while True:
        angReq = min(angMax,
                     max(angMin,
                         int(input("Reqested angle :"))))
        f.ChangeDutyCycle(getDucy(angReq))

def destroy():
    f.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    print("Programm starting...")
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
