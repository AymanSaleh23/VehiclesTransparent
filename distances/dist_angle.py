
import time

import RPi.GPIO as GPIO
class Angles:
    def __init__(self, servo_pin):
        servoPIN = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        self.servo_pin = servo_pin
        
        # GPIO 17 for PWM with 50Hz
        self.pwm_ch = GPIO.PWM(servo_pin, 50) 
        self.pwm_ch.start(2.5) # Initialization
        
    def set_angle(self, angle):
        try:    
            pwm_ch.ChangeDutyCycle(map_values_ranges(angle, 0, 180, 2, 12) )
            time.sleep(0.5)            

        except Exception:
            pwm_ch.stop()