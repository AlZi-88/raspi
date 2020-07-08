from time import *
from RPi import GPIO
from ADCDevice import *

adc = ADCDevice()
pwmPin = 11

def setup():
    global adc
    if adc.detectI2C(0x48):
        adc=PCF8591()
    elif adc.detectI2C(0x4b):
        adc =ADS7830()
    else:
        print("No correct I2C address found \n"
              "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
              "Programm exit. \n")
        exit(-1)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pwmPin, GPIO.OUT)
    global f
    f = GPIO.PWM(pwmPin, 1000)
    f.start(0)
    
def loop():
    while True:
        value = adc.analogRead(0)
        voltage = value / 255.0 * 3.3
        print("ADC Value: {}, Voltage: {}V".format(value, voltage))
        f.ChangeDutyCycle(int(value/2.55))
        sleep(0.1)

def destroy():
    adc.close()


if __name__ == "__main__":
    print("Programm starting...")
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
        
