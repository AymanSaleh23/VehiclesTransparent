from gpiozero import Servo
from time import sleep

"""
        Class:
          NAME            :  ServoMotor
          DESCRIPTION     :  A class to control angle of servo motor
          CLASS ATTRIBUTE :  None
          DUNDER METHODS  :  __init__
          METHODS         :  move_to
          MAX NO. Objects :  None
    """


class ServoMotor:
    def __init__(self, pin_number=17,correction=0):
        self.pin_number = pin_number
        self.myCorrection = correction
        max_pw = (2.0 + self.myCorrection) / 1000
        min_pw = (1.0 - self.myCorrection) / 1000
        self.servo = Servo(self.pin_number, min_pulse_width=min_pw, max_pulse_width=max_pw)

    # Name   : move_to
    # input  : value parameter should be between [ 0 : 20 ]
    # output : move servo motor to specific angle
    def move_to(self, value):
        self.servo.value = value
        print(value)
        sleep(0.5)
