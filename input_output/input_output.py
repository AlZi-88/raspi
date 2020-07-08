from RPi import GPIO
from time import sleep

ledPin = 11
pwmPin = 12
switchPin = 12
stateLed = False

def setup():

#    global f_pwm
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
#    GPIO.setup(pwmPin, GPIO.OUT)
    GPIO.setup(switchPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#    f_pwm = GPIO.PWM(pwmPin, 500)
#    f_pwm.start(0)
    GPIO.output(ledPin, False)


def buttonEvent(channel):
      
#    global stateLed
#    print(stateLed)
    if GPIO.input(switchPin) == False:
        #stateLed = not stateLed
        GPIO.output(ledPin, True)
    else:
        GPIO.output(ledPin, False)
            
    

def loop():
    GPIO.add_event_detect(switchPin,
                          GPIO.FALLING,
                          callback = buttonEvent,
                          bouncetime = 300)
##    while True:
##        for ducy_led in range(101):
##            f_pwm.ChangeDutyCycle(ducy_led)
##            sleep(0.01)
##        sleep(1)
##        for ducy_led in range(100,-1,-1):
##            f_pwm.ChangeDutyCycle(ducy_led)
##            sleep(0.01)
##        sleep(1)
        
def destroy():
#    f_pwm.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    print("Program is starting")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
