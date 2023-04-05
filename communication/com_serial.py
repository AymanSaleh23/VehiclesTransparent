import serial, time, json

class SerialComm:
    def __init__(self, name, port="COM4", parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                 bytesize=serial.EIGHTBITS, baudrate=9600, timeout=1):
        self.parity, self.stopbits = parity, stopbits
        self.bytesize, self.port = bytesize, port
        self.baudrate, self.timeout = baudrate, timeout
        self.name = name
        self.serial_command = "0"
        self.connection_state = False
        self.received_data = None
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout, parity=self.parity,
                                     stopbits=self.stopbits, bytesize=self.bytesize)
            self.ser.flush()
            while not self.ser.isOpen():
                print(f"Can't Open Serial: {self.__str__()}")
                self.ser.open()
            else:
                self.ser.setDTR(False)
                self.ser.flushInput()
                self.ser.setDTR(True)
                self.ser.reset_input_buffer()
                self.connection_state = True
                print(f"Serial Initialized: {self.__str__()}")
                time.sleep(1)
                return
        except Exception:
            self.ser = None
            self.connection_state = False
            print("Failed Initialization Serial")

    def send_query(self, data_query):
        if self.connection_state:
            try:
                # Encode the data as JSON
                json_data = json.dumps(data_query) + '\n'
                encoded_data = json_data.encode(encoding='utf-8')
                self.ser.write(encoded_data)

                print(f">>>Serial Debug Command: {data_query}")

            except Exception:
                print("Communication Breaked & Reading")
                print("Serial Closed")
                self.connection_state = False
                self.ser = None

        else:
            print("Communication Status is False")
            self.ser = None
            self.__init__(name=self.name, port=self.port, parity=self.parity, stopbits=self.stopbits,
                          bytesize=self.bytesize,
                          baudrate=self.baudrate, timeout=self.timeout)
            self.connection_state = True
            print(f"Restarting Serial: {self.__str__()}")

    def receive_query(self):
        to_return = {"ORIENT": [-1, -1, -1],
                     "DISTANCE": [-1, -1, -1]}
        if self.connection_state:
            try:
                while self.ser.in_waiting > 0:

                    # Wait for a response from the serial device
                    response = self.ser.readline()
                    # Decode the response from JSON
                    decoded_response = response.decode()
                    # Load the Decoded response from json
                    loaded_data = json.loads(decoded_response)
                    if loaded_data != self.received_data:
                        self.received_data = loaded_data

                print(">>>Serial Debug Receive: ", self.received_data)
                to_return = self.received_data

            except Exception:
                print("Communication Breaked & Reading")
                print("Serial Closed")
                self.connection_state = False
                self.ser = None
                to_return = {"ORIENT": [-1, -1, -1], "DISTANCE": [-1, -1, -1]}
        else:
            print("Communication Status is False")
            self.ser = None
            self.__init__(name=self.name, port=self.port, parity=self.parity, stopbits=self.stopbits,
                          bytesize=self.bytesize,
                          baudrate=self.baudrate, timeout=self.timeout)
            self.connection_state = True
            print(f"Restarting Serial: {self.__str__()}")

        return to_return

    def __str__(self):
        return f"NAME:{self.name}, PORT:{self.port}, Baudrate:{self.baudrate}, TimeOut:{self.timeout}"
