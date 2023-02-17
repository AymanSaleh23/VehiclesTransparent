import serial
import time 

class SerialComm:
    def __init__(self, port="COM4", parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS, baudrate=9600, timeout=1):
        self.parity, self.stopbits = parity, stopbits
        self.bytesize, self.port = bytesize, port
        self.baudrate, self.timeout = baudrate, timeout

        self.serial_command = "0"
        self.connection_state = False
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout, parity=self.parity,
                                     stopbits=self.stopbits, bytesize=self.bytesize)
            self.ser.flush()
            if not self.ser.isOpen():
                self.ser.open()
            else:
                self.ser.setDTR(False)
                self.ser.flushInput()
                self.ser.setDTR(True)
                self.ser.reset_input_buffer()
                self.connection_state = True
                self.received_data = None
                print(f"Serial Initialized: {self.__str__()}")
                time.sleep(3)
                return
        except Exception:
            self.ser = None
            self.connection_state = False
            print("Failed Initialization Serial")

    def get_value(self):
        if self.connection_state:
            try:
                self.ser.write(self.serial_command.encode(encoding='utf-8'))
                print(f"Command: {self.serial_command}") 
                time.sleep(2)
                if self.ser.in_waiting > 0:
                    self.received_data = self.ser.readline().decode('utf-8')
                    print("Debug Receive: ", self.received_data)
                    
                    return self.received_data
                
            except Exception:
                print("Communication Breaked & Reading")
                print("Serial Closed")
                self.connection_state = False
                self.ser = None

        else:
            print("Communication Status is False")
            self.ser = None
            self.__init__(port=self.port, parity=self.parity, stopbits=self.stopbits, bytesize=self.bytesize,
                          baudrate=self.baudrate, timeout=self.timeout)            
            self.connection_state = True
            print(f"Restarting Serial: {self.__str__()}")
    
    def __str__ (self):
        return f"PORT:{self.port}, Baudrate:{self.baudrate}, TimeOut:{self.timeout}"
