import RPi.GPIO as GPIO
import time


class Measure:
    
    total_unit = 0

    def __init__(self, trig, echo):
        if Measure.total_unit < 3:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            
            # two arguments number of trig and echo in GPIO
            self.trig.append(list(trig))
            self.echo.append(list(echo))
            GPIO.setup(trig,GPIO.OUT)
            GPIO.setup(echo,GPIO.IN)
            Measure.total_unit +=1
        else:
            print("not available to add more than 3 measuring units...!")

    # Return distance between ultrasonic and object
    def distance_read(self):
        GPIO.output(self.trig,False)
        time.sleep(1)
        GPIO.output(self.trig,True)
        time.sleep(0.000002)
        GPIO.output(self.trig,False)

        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()
    
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()
    
        pulse_duration = pulse_end - pulse_start
        distance = (pulse_duration * 35124)/2
        distance = round(distance, 2)
        return distance

"""
#########   Test     ##########
u1 = Measure(12, 19)
u2 = Measure(13, 20)
u3 = Measure(14, 21)

for i in range(50):

    u1.distance_read()
    u2.distance_read()
    u3.distance_read()
"""

