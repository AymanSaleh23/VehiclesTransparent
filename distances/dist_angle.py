
import time
from mathematics import mathlib
import RPi.GPIO as GPIO
class Angles:
    def __init__(self, servo_pin):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo_pin, GPIO.OUT)
        self.servo_pin = servo_pin
        
        # GPIO 17 for PWM with 50Hz
        self.pwm_ch = GPIO.PWM(servo_pin, 50) 
        self.pwm_ch.start(2.5) # Initialization
        
    def set_angle(self, angle):
        self.pwm_ch.ChangeDutyCycle(mathlib.map_values_ranges(angle, 180, 0, 2, 12))
        time.sleep(0.5)
