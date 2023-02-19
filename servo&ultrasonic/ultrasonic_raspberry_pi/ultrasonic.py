
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# two arguments number of trig and encho in GPIO
trig = 16
echo = 18
# inti configration for ultrasonic set trig as output and echo as input
def ultrasonic_init():
	global trig,echo
	print('distane mesurement in progress')
	#set gpio configration
	GPIO.setup(trig,GPIO.OUT)    # trig is ouput 
	GPIO.setup(echo,GPIO.IN)	  # echo is input 
	
#return distance between ultrasonic and object   
def ultrasonic_read():
	global trig , echo
	
	GPIO.output(trig,False)
	time.sleep(1)
	GPIO.output(trig,True)
	time.sleep(0.000002)
	GPIO.output(trig,False)
	
	while GPIO.input(echo)==0 :
		pulse_start=time.time()

	while GPIO.input(echo)==1 :
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = (pulse_duration * 35124)/2
	distance = round(distance ,2 )
	return distance


ultrasonic_init()

for i in range(50):

	distance =ultrasonic_read()
	print ('distance is '+ str(distance)+ ' cm ')

