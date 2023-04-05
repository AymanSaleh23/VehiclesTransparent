from rpi_app.distances.dist_measure import Measure
import time
u1 = Measure(27, 22)
u2 = Measure(23, 24)
u3 = Measure(5, 6)

while True:
      print(f"u1: {u1.distance_read()}cm")
      print(f"u2: {u2.distance_read()}cm")
      print(f"u3:{ u3.distance_read()}cm")
      time.sleep(0.1)
