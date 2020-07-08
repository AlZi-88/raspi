from time import *
from RPi import GPIO
from ADCDevice import *
from math import *

adc = ADCDevice()
r_pu = 10000    #Ohm
V_sup = 3.3       #V
R_nom = 10000   #Ohm
B = 3950        #thermal index
T_nom = 25         #°C nominal Temperature

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

    
def loop():
    while True:
        value = adc.analogRead(0)
        voltage = value / 255.0 * 3.3
        R_temp = r_pu/(V_sup/voltage-1)
        temp = 1/(1/(T_nom+273.15) + log(R_temp/R_nom)/B)-273.15
        print("ADC Value: {}, Voltage: {:.2f}V, Resistance: {:.2f}Ohm, Temp: {:.2f}°C".format(value, voltage, R_temp, temp))
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
