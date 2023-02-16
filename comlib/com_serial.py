import serial
import time 

class SerialComm:
    def __init__(self, port="COM4", baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection_state = False
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.ser.setDTR(False)
            time.sleep(1)
            self.ser.flushInput()
            self.ser.setDTR(True)
            time.sleep(2)
            self.ser.reset_input_buffer()
            self.connection_state = True
            self.received_data = None
            print("Serial Initialized")
        except Exception:
            print("Failed Initialization Serial")
        

    def get_value(self):
        print("0")
        if self.connection_state == True:
            print("1")
            try:
                print("2")
                if self.ser.in_waiting > 0:
                    print("3")
                    self.received_data= self.ser.read().decode('utf-8')
                    print("Debug Receive: ", self.received_data)
                    return self.received_data
                
            except Exception :
                print("4")
                print("Serial Closed")
                self.connection_state = False
                self.ser.close()
        else :
            print("5")
            self.__init__(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            print ("Restart Serial")
