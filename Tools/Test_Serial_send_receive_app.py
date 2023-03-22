from communication.com_serial import *
from threading import Thread

sc = SerialComm(port="COM11", name="Sender", baudrate=115200)
print(sc)
a, b, c = 0, 0, 0

def fetcher():
    dist_list = []
    while True:
        temp_holder = sc.receive_query()
        if temp_holder is not None:
            dist_list = [section for section in temp_holder]
        print(f"Test_App: {dist_list}, Length={len(dist_list)}")
        time.sleep(0.1)


t = Thread(target=fetcher, args=[], daemon=True)
t.start()

while True:
    a, b, c = a+1, b+1, c+1
    sc.send_query(data_query=[a, b, c])
    time.sleep(0.4)
    print("main App")

