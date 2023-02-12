"""     Test Serial App """
sc = SerialComm(port='COM4', baudrate=115200, timeout=1)

while True:
    print(">>>From App:", sc.get_value())
    time.sleep(0.5)
    print ("Any Other app!!!")
    time.sleep(2)