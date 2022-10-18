 import RPi.GPIO as gp  
 from time import sleep,time  
 import LiquidCrystal_I2C  
 lcd=LiquidCrystal_I2C.lcd()  
 gp.setmode(gp.BOARD)  
 gp.setup(16,gp.OUT)  
 gp.setup(15,gp.IN)  
 lcd.clear()  
 lcd.display("Measuring",1,4)  
 lcd.display("Distance",2,4)  
 sleep(1)  
 lcd.clear()  
 gp.output(16,gp.LOW)  
 sleep(0.000002)  
 global st,sto  
 lcd.display("Distance:",1,1)  
 while True:  
   try:  
     gp.output(16,True)  
     sleep(0.00001)  
     gp.output(16,False)  
     while gp.input(15)==0:  
       st=time()  
       #print(st,"\n")  
     while gp.input(15)==1:  
       sto=time()  
       #print(sto)  
     tt=sto-st  
     dist=(tt*35124)/2 # in place of 35124 enter your spped of sound on basis of tempreature  
     dist=round(dist,3)  
     lcd.display("%f"%(dist),2,4)  
   except KeyboardInterrupt:  
     lcd.clear()  
     gp.cleanup()  
     break  