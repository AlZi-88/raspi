from time import *
from RPi import GPIO
from ADCDevice import *
from math import *

motorPins = {"A":12, "B":16, "C":18, "D":22}
forward = ["A", "B", "C", "D"]
backward = ["D", "C", "B", "A"]
motorGearRatio = 64     #1 rotation of stepper motor requires 64 motor rotations
numberCoils = 32
numberPhases = len(motorPins)
directions = ("forward", "backward")
deg_per_step = 360/motorGearRatio/numberCoils
speedMax = deg_per_step/(1.7*0.001)       #deg/s


def setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in motorPins.values():
        GPIO.setup(pin, GPIO.OUT)

def angle2cycles(angle):
    motorAngle = motorGearRatio*angle
    rotations = motorAngle / 360
    cycles = int(rotations * 32)
    return cycles

def getSequence(angle, direction_seqence):
    cycles = angle2cycles(angle)
    seq = []
    numberCyc = (cycles // numberPhases)
    rest = int(round(cycles%numberPhases))
    seq = numberCyc*direction_seqence
    for i in range(rest):
        seq.append(forward[i])
    return seq

def move(angle, speed, direction):
    if direction == "forward":
        phaseSequence = getSequence(angle, forward)
    elif direction == "backward":
        phaseSequence = getSequence(angle, backward)
    print(len(phaseSequence))
    print(phaseSequence)
    for activePhase in phaseSequence:
        for phase, pin in motorPins.items():
            GPIO.output(pin, phase == activePhase)
        sleep(deg_per_step/min(speed, speedMax))

def motorStop():
    for pin in motorPins.values():
        GPIO.output(pin, GPIO.LOW)

def destroy():
    GPIO.cleanup()

def loop():
    while True:
        angle_sp = 360      #deg
        t1 = time() 
        move(angle_sp, 0.95*speedMax, "forward")
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
        move(angle_sp, 0.95*speedMax, "backward")
        #motorStop()     
        sleep(0.5)

if __name__ == "__main__":
    print("Programm starting...")
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
