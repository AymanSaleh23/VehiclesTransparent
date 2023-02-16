"""     Test Serial App """
sc = SerialComm(port='COM5', baudrate=115200, timeout=1)

while True:
    sc.serial_command = "1"
    print(">>>From App:", sc.get_value())
    sc.serial_command = "2"
    print(">>>From App:", sc.get_value())
    time.sleep(0.5)
    print("Any Other app!!!")
    time.sleep(2)