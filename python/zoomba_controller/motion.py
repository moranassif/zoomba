# This class provides basic methods for moving around

import RPi.GPIO as GPIO
import time

class motion(object):
    """Provides inteface for moving the zoomba around
    """
    def __init__(self):
        self.PWM_PIN = 18
        self.MODE_PIN = 17
        self.DIRECTION_L_PIN = 4
        self.DIRECTION_R_PIN = 24

        GPIO.setup(self.PWM_PIN, GPIO.OUT)
        GPIO.setup(self.MODE_PIN, GPIO.OUT)
        GPIO.setup(self.DIRECTION_L_PIN, GPIO.OUT)
        GPIO.setup(self.DIRECTION_R_PIN, GPIO.OUT)

        GPIO.setmode(GPIO.BCM)

        # Set mode to PWM
        GPIO.OUTPUT(self.MODE_PIN, 1)
        self.pwm = GPIO.PWM(self.PWM1_PIN, 50)

    def turn(self, direction, degrees):
        """Turns the bot the direction and degrees given as arguments
        """
        if direction == "left":
            GPIO.OUTPUT(self.DIRECTION_L_PIN, 1)
            GPIO.OUTPUT(self.DIRECTION_R_PIN, 0)
        elif direction == "right":
            GPIO.OUTPUT(self.DIRECTION_L_PIN, 0)
            GPIO.OUTPUT(self.DIRECTION_R_PIN, 1)
        else: raise Exception("Cannot turn to direction %s, options are 'left' and 'right'" % direction)
        
        self.pwm.start(10)
        time.sleep(degrees/10)
        self.pwm.stop()
        
    def advance(self, direction, time):
        """Tells the bot the advance to direction given for the given time
        """
        if direction == "forward":
            GPIO.OUTPUT(self.DIRECTION_L_PIN, 1)
            GPIO.OUTPUT(self.DIRECTION_R_PIN, 1)
        elif direction == "backward":
            GPIO.OUTPUT(self.DIRECTION_L_PIN, 0)
            GPIO.OUTPUT(self.DIRECTION_R_PIN, 0)
        else: Exception("Cannot advance to direction %s, options are 'forward' and backward" % direction)
        
        self.pwm.start(10)
        time.sleep(time)
        self.pwm.stop()
            
    def __del__(self):
        """Cleans up the GPIOs
        """
        GPIO.cleanup()
