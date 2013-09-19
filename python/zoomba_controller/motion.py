# This class provides basic methods for moving around

import RPi.GPIO as GPIO
import time

class motion(object):
    """Provides inteface for moving the zoomba around
    """
    def __init__(self):
       self.PWM_PIN = 18
       self.MODE_PIN = 25
       self.DIRECTION_L_PIN = 23
       self.DIRECTION_R_PIN = 24

       self.SENSOR_FORWARD_PIN = 17
       self.SENSOR_LEFT_PIN = 4
       self.SENSOR_RIGHT_PIN = 22

       GPIO.setmode(GPIO.BCM)

       GPIO.setup(self.PWM_PIN, GPIO.OUT)
       GPIO.setup(self.MODE_PIN, GPIO.OUT)

       GPIO.setup(self.DIRECTION_L_PIN, GPIO.OUT)
       GPIO.setup(self.DIRECTION_R_PIN, GPIO.OUT)

       # Set mode to PWM
       GPIO.output(self.MODE_PIN, 1)
       self.pwm = GPIO.PWM(self.PWM_PIN, 50)

       # Set sensors
       GPIO.setup(self.SENSOR_FORWARD_PIN, GPIO.IN)
       GPIO.setup(self.SENSOR_LEFT_PIN, GPIO.IN)
       GPIO.setup(self.SENSOR_RIGHT_PIN, GPIO.IN)

       GPIO.add_event_detect(self.SENSOR_FORWARD_PIN, GPIO.RISING, callback=self.got_button, bouncetime=200)
       GPIO.add_event_detect(self.SENSOR_LEFT_PIN, GPIO.RISING, callback=self.got_button, bouncetime=200)
       GPIO.add_event_detect(self.SENSOR_RIGHT_PIN, GPIO.RISING, callback=self.got_button, bouncetime=200)

       # time stamp to help debounce buttons
       self.time_stamp = 0
       self.handling_got_button = False

       # Sets the motion state
       self.state = "forward"

    def turn(self, direction, degrees):
        """Turns the bot the direction and degrees given as arguments
        """
        if direction == "left":
            GPIO.output(self.DIRECTION_L_PIN, 1)
            GPIO.output(self.DIRECTION_R_PIN, 0)
        elif direction == "right":
            GPIO.output(self.DIRECTION_L_PIN, 0)
            GPIO.output(self.DIRECTION_R_PIN, 1)
        else: raise Exception("Cannot turn to direction %s, options are 'left' and 'right'" % direction)

        self.pwm.start(50)
        time.sleep(degrees/10)
        self.pwm.stop()

    def advance(self, direction, go_time):
        """Tells the bot the advance to direction given for the given time
        """
        if direction == "forward":
            GPIO.output(self.DIRECTION_L_PIN, 0)
            GPIO.output(self.DIRECTION_R_PIN, 0)
        elif direction == "backward":
            GPIO.output(self.DIRECTION_L_PIN, 1)
            GPIO.output(self.DIRECTION_R_PIN, 1)
        else: Exception("Cannot advance to direction %s, options are 'forward' and backward" % direction)

        self.pwm.start(50)
        time.sleep(go_time)
        self.pwm.stop()

    def got_button(self, channel):
        """React to the pressing of a sensor
        """
        if not self.handling_got_button:
            self.handling_got_button = True
            press_time = time.time()
            # Handle debounce
            if press_time - self.time_stamp > 0.3:
                print "Handling sensor. Press time is %d and stamp time is %d" %(press_time, self.time_stamp)
                self.time_stamp = press_time + 1000
                if channel == self.SENSOR_FORWARD_PIN:
                    print "Got signal from forward sensor"
                    self.state = "backward"
                    time.sleep(3)
                    self.state = "turn_left"
                    time.sleep(2)
                    self.state = "forward"
                if channel == self.SENSOR_LEFT_PIN:
                    print "Got signal from left sensor"
                    self.state = "backward"
                    time.sleep(3)
                    self.state = "turn_right"
                    time.sleep(2)
                    self.state = "forward"
                if channel == self.SENSOR_RIGHT_PIN:
                    print "Got signal from right sensor"
                    self.state = "backward"
                    time.sleep(3)
                    self.state = "turn_left"
                    time.sleep(2)
                    self.state = "forward"
                print "Finishing handling button"
                self.time_stamp = press_time
                self.handling_got_button = False

    def do_nothing(self):
        print "Waiting for something to happen"
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print "Got keyboard interrupt"
            GPIO.cleanup()

    def drive(self):
        """Going foward until hitting a wall
        """
        try:
            while True:
                if   self.state == "forward":
                    self.advance("forward", 0.5)
                elif self.state == "backward":
                    self.advance("backward", 0.5)
                elif self.state == "turn_left":
                    self.turn("left", 10)
                elif self.state == "turn_right":
                    self.turn("right", 10)
                else:
                    GPIO.cleanup()
                    raise Exception("Unknown state %s" % self.state)
        except KeyboardInterrupt:
            print "Got keyboard interrupt"
            GPIO.cleanup()

    def __del__(self):
        """Cleans up the GPIOs
        """
        GPIO.cleanup()
