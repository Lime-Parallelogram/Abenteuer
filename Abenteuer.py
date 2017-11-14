#/usr/bin/python

#------Imports Modules------#
import RPi.GPIO as GPIO
import spidev

#------Pin Declarations------#
headlights = 11
motor_controll = [13,16,18,3]

#------Program setup declarations------#
MainBatCh = 0
SecondaryBatCh = 1

#------Other Vars------#
motor_PWMs = []
reverse = False

#------Initialise pins------#
def init():
    global headlights
    global spi
    global motor_controll
    global motor_PWMs
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(headlights, GPIO.OUT)
    spi = spidev.SpiDev()
    spi.open(0, 0)
    for i in range(4):
        print(i)
        GPIO.setup(motor_controll[i],GPIO.OUT)
        motor_PWMs.append(GPIO.PWM(motor_controll[i], 50))
        motor_PWMs[i].start(0)
        

#------Change Speed------#
def thrust(cycle):
    global motor_PWMs
    global reverse
    if reverse:
        motor_PWMs[0].ChangeDutyCycle(0)
        motor_PWMs[2].ChangeDutyCycle(0)
        motor_PWMs[1].ChangeDutyCycle(cycle)
        motor_PWMs[3].ChangeDutyCycle(cycle)
    else:
        motor_PWMs[0].ChangeDutyCycle(cycle)
        motor_PWMs[2].ChangeDutyCycle(cycle)
        motor_PWMs[1].ChangeDutyCycle(0)
        motor_PWMs[3].ChangeDutyCycle(0)
        
#------Lighting controll class------#
class lights:
    global headlights
    #------Turn On/Off headlights------#
    def headlight(state):
        GPIO.output(headlights, state)

#------Battery Measuring class------#
class batterys:
    def get_main_volts():
        global MainBatCh
        global spi
        r = spi.xfer2([1, 8 + MainBatCh << 4, 0])
        data = ((r[1] & 3) << 8) + r[2]
        percent = int(round(data/10.24))
        return percent
    def get_secondary_volts():
        global SecondaryBatCh
        global spi
        r = spi.xfer2([1, 8 + SecondaryBatCh << 4, 0])
        data = ((r[1] & 3) << 8) + r[2]
        percent = int(round(data/10.24))
        return percent

#------Test------#
init()
lights.headlight(True)
print(str(batterys.get_secondary_volts()))
reverse = True
thrust(100)
