"""     Test Serial App """
import threading, time
from communication.com_serial import SerialComm

sc = SerialComm(port='COM4', baudrate=115200, timeout=1)
def test_ser():
    while True:
        print(">>>From App:", sc.send_query())
        time.sleep(0.5)

t1 = threading.Thread(target=test_ser, args=[])
t1.start()

while True:
    print ("Any Other app!!!")
    time.sleep(2)