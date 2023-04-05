import time

from communication.com_serial import SerialComm
from threading import Thread


sc = SerialComm(port="COM9", name="Receiver", baudrate=115200)
print(sc)


def fetcher():
    dist_list = []
    while True:
        temp_holder = sc.receive_query()
        if temp_holder:
            dist_list = [section for section in sc.receive_query()]
        print(f"Test_App: {dist_list}, Length={len(dist_list)}")
        time.sleep(0.1)


t = Thread(target=fetcher, args=[], daemon=True)
t.start()
while True:
    time.sleep(1)

    print("main App")

