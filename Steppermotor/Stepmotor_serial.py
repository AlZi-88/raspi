from time import *
from RPi import GPIO
from ADCDevice import *
from math import *
from Stepmotor import *

dataPin = 11
latchPin = 13
clockPin = 15
LSBFIRST = True
MSBFIRST = not LSBFIRST
map2serial = {"A":[0,0,0,0,0,0,0,1],
              "B":[0,0,0,0,0,0,1,0],
              "C":[0,0,0,0,0,1,0,0],
              "D":[0,0,0,0,1,0,0,0]}

motorPins = {"A":12, "B":16, "C":18, "D":22}
forward = ["A", "B", "C", "D"]
backward = ["D", "C", "B", "A"]
motorGearRatio = 64     #1 rotation of stepper motor requires 64 motor rotations
numberCoils = 32
numberPhases = len(motorPins)
directions = ("forward", "backward")
deg_per_step = 360/motorGearRatio/numberCoils
speedMax = deg_per_step/(1.7*0.001)       #deg/s


def setupSerial():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(dataPin, GPIO.OUT)
    GPIO.setup(latchPin, GPIO.OUT)
    GPIO.setup(clockPin, GPIO.OUT)
    if MSBFIRST:
        for bits in map2serial.values():
            bits.reverse()

def sendSerial(activePhase):
    GPIO.output(latchPin, GPIO.LOW)
    for bit in map2serial[activePhase]:
        GPIO.output(clockPin, GPIO.LOW)
        GPIO.output(dataPin, bit==1)
        GPIO.output(clockPin, GPIO.HIGH)
    GPIO.output(latchPin, GPIO.HIGH)

def moveSerial(angle, speed, direction):
    if direction == "forward":
        phaseSequence = getSequence(angle, forward)
    elif direction == "backward":
        phaseSequence = getSequence(angle, backward)
    print(len(phaseSequence))
    print(phaseSequence)
    for activePhase in phaseSequence:
        sendSerial(activePhase)
        sleep(deg_per_step/min(speed, speedMax))

def serialLoop():
    while True:
        angle_sp = 360      #deg
        t1 = time() 
        moveSerial(angle_sp, 0.95*speedMax, "forward")
        t2 = time()
        dt = t2-t1
        print(dt, "s for ",
              angle_sp,
              "deg, makes speed of ",
              round(angle_sp/dt, 2),
              "deg/s, speed max ",
              speedMax,
              " deg/s")
        #motorStop()
        sleep(0.5)
        moveSerial(angle_sp, 0.95*speedMax, "backward")
        #motorStop()     
        sleep(0.5)

if __name__ == "__main__":
    print("Programm starting...")
    try:
        setupSerial()
        serialLoop()
    except KeyboardInterrupt:
        destroy()
