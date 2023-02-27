import os
import time
from threading import Thread

if __name__ == "__main__":
    t_cv = Thread(target=os.system, args=["python main.py"])
    t_m = Thread(target=os.system, args=["python measure_app.py"])

    t_cv.setDaemon(True)
    t_m.setDaemon(True)

    t_cv.start()
    t_m.start()

    while True:
        time.sleep(1)