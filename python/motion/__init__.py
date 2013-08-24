# This class provides basic methods for moving around

import RPi.GPIO as GPIO
import time

class motion(object):
    """Provides inteface for moving the zoomba around
    """
    def __init__(self):
        self.PWM_PIN = 18
        self.MODE_PIN = 17
        self.DIRECTION1_PIN = 4
        self.DIRECTION2_PIN = 24

        GPIO.setup(PWM_PIN, GPIO.OUT)
        GPIO.setup(MODE_PIN, GPIO.OUT)
        GPIO.setup(DIRECTION1_PIN, GPIO.OUT)
        GPIO.setup(DIRECTION2_PIN, GPIO.OUT)

        GPIO.setmode(GPIO.BCM)




# Set mode to PWM
GPIO.output(MODE_PIN,1)

#pwm = GPIO.PWM(PWM_PIN, 2)
#pwm.start(1)
#raw_input('Press return to stop:')
#pwm.stop()
#GPIO.cleanup()

p1 = GPIO.PWM(PWM1_PIN, 50)
p2 = GPIO.PWM(PWM2_PIN, 50)
p1.start(0)
p2.start(0)
try:
    while 1:
	for dc in range(0, 101, 5):
	    p1.ChangeDutyCycle(dc)
	    p2.ChangeDutyCycle(dc)
	    time.sleep(0.1)
	for dc in range(100, -1, -5):
	    p1.ChangeDutyCycle(dc)
	    p2.ChangeDutyCycle(dc)
	    time.sleep(0.1)
except KeyboardInterrupt:
    pass
p1.stop()
p2.stop()
GPIO.cleanup()
