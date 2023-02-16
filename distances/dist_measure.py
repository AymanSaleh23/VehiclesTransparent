import RPi.GPIO as GPIO
import time


class Measure:
    
    total_unit = 0
    TIME_OUT = 3
    __TIME_FAKE = 0
    __TIME_TRUE = 1
    
    def __init__(self, trig, echo):
        if Measure.total_unit < 3:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            # two arguments number of trig and echo in GPIO
            self.trig = trig
            self.echo = echo
            self.pulse_start = 0
            self.pulse_end = 0
            self.pulse_duration = 0
            self.duration = 0
            self.distance = 0
            self.time_status = None
            GPIO.setup(trig,GPIO.OUT)
            GPIO.setup(echo,GPIO.IN)
            Measure.total_unit +=1
        else:
            print("not available to add more than 3 measuring units...!")

    # Return distance between ultrasonic and object
    def distance_read(self):
        GPIO.output(self.trig,False)
        time.sleep(0.001)
        GPIO.output(self.trig,True)
        time.sleep(0.000002)
        GPIO.output(self.trig,False)

        self.time_status = Measure.__TIME_FAKE
        init_t_1 = time.time()
        
        while GPIO.input(self.echo) == 0 and self.pulse_start - init_t_1 < Measure.TIME_OUT:
            self.pulse_start = time.time()
        
        init_t_2 = time.time()
        while GPIO.input(self.echo) == 1 and self.pulse_end  - init_t_2 < Measure.TIME_OUT:
            self.pulse_end = time.time()
    
        if self.pulse_start - init_t_1 > Measure.TIME_OUT or self.pulse_end  - init_t_2 > Measure.TIME_OUT:
            self.time_status = Measure.__TIME_FAKE
            self.distance = None
            
        else :
            self.time_status = Measure.__TIME_TRUE
            self.pulse_duration = self.pulse_end - self.pulse_start
            self.distance = (self.pulse_duration * 34000)/2
            self.distance = round(self.distance, 2)
            self.distance = [self.distance if self.time_status == Measure.__TIME_TRUE else Measure.__TIME_FAKE in [0]].pop()
        return self.distance

